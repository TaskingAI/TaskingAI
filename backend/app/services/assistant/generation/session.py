from abc import ABC
from .utils import *
from .log import *
from app.models import MessageRole, MessageContent, Model, Assistant, Chat, Tool, ToolInput, ToolOutput
from app.services.assistant.message import create_message
from app.services.model import get_model
from app.services.tool import run_tools, fetch_tools
from app.services.inference.chat_completion import chat_completion
from tkhelper.utils import check_http_error
import logging

logger = logging.getLogger(__name__)


class Session(ABC):
    def __init__(self, assistant: Assistant, chat: Chat):
        # assistant
        self.assistant: Assistant = assistant
        self.chat: Chat = chat

        # tools
        self.tool_dict: Dict[str, Tool] = {}
        self.tool_use_count: Dict[str, List[int]] = {}
        self.max_tool_use_count = 5

        # retrievals
        self.retrieval_tool_name = None
        self.retrieval_collection_ids = None

        # model
        self.model: Model = None

        # chat memory
        self.chat_memory_messages = None

        # chat completion parameters
        self.system_prompt = None
        self.chat_completion_messages = None
        self.chat_completion_functions = []

        # id
        self.session_id = generate_random_session_id()

        self.prepare_logs = []

    async def create_assistant_message(self, content_text: str):
        return await create_message(
            assistant_id=self.assistant.assistant_id,
            chat_id=self.chat.chat_id,
            role=MessageRole.ASSISTANT,
            content=MessageContent(text=content_text),
            metadata={},
        )

    async def prepare(self, stream: bool, system_prompt_variables: Dict, retrieval_log: bool = False):
        # check chat lock
        if await self.chat.is_chat_locked():
            raise MessageGenerationException(f"Chat {self.chat.chat_id} is locked. Please try again later.")

        # 1. Get model
        self.model = await get_model(self.assistant.model_id)

        # 2. model streaming
        if not self.model.allow_streaming() and stream:
            raise MessageGenerationException(f"Assistant model {self.model.model_id} does not support streaming. ")

        # 3. Get chat memory
        self.chat_memory_messages = await get_chat_memory_messages(self.chat)
        logger.debug(f"Chat memory: {self.chat_memory_messages}")

        # 4. Get tools
        if self.assistant.tools:
            tools = await fetch_tools(self.assistant.tools)
            self.tool_dict = {tool.function_name(): tool for tool in tools}
            self.chat_completion_functions = [tool.function_def for tool in tools]
            logger.debug(f"Tool functions fetched: {self.chat_completion_functions}")

        # 5. Get retrievals
        retrieval_doc = None

        if self.assistant.retrievals:
            self.retrieval_collection_ids = [
                retrieval.id for retrieval in self.assistant.retrievals if retrieval.type == "collection"
            ]

            if self.assistant.retrieval_configs.method != RetrievalMethod.FUNCTION_CALL:
                # build query text and query retrieval collections
                retrieval_query_text = get_system_prompt_retrieval_query_text(
                    chat_memory_messages=self.chat_memory_messages,
                    method=self.assistant.retrieval_configs.method,
                )
                if retrieval_query_text:
                    retrieval_event_id = generate_random_event_id()
                    if retrieval_log:
                        retrieval_log_input = build_retrieval_input_log_dict(
                            session_id=self.session_id,
                            event_id=retrieval_event_id,
                            query_text=retrieval_query_text,
                            top_k=self.assistant.retrieval_configs.top_k,
                        )
                        self.prepare_logs.append(retrieval_log_input)

                    retrieval_doc, retrieval_results = await query_assistant_retrieval(
                        assistant=self.assistant,
                        query_text=retrieval_query_text,
                    )

                    if retrieval_log:
                        retrieval_log_output = build_retrieval_output_log_dict(
                            session_id=self.session_id,
                            event_id=retrieval_event_id,
                            retrieval_result=retrieval_results,
                        )
                        self.prepare_logs.append(retrieval_log_output)

            else:
                # make retrieval a function
                retrieval_function = build_retrieval_function_dict(
                    existing_tool_names=list(self.tool_dict.keys()),
                    description=self.assistant.retrieval_configs.function_description,
                )
                self.retrieval_tool_name = retrieval_function["name"]
                self.chat_completion_functions.append(retrieval_function)

        # 7. Build system prompt
        self.system_prompt = build_system_prompt(
            system_prompt_template=self.assistant.system_prompt_template,
            system_prompt_variables=system_prompt_variables or {},
            # context_summary=self.chat_memory_context_summary,
            retrieval_doc=retrieval_doc,
        )
        self.chat_completion_messages = build_chat_completion_messages(
            system_prompt=self.system_prompt,
            history_messages=self.chat_memory_messages,
        )

    async def use_tool(self, function_calls, round_index: int, log=False):
        """
        use tool and count the use times
        :param function_calls: function call dict received from chat completion
        :param round_index: current round index
        :param log: whether to log the tool action call
        :return: tool action call log dict if log is True else None
        """

        logs = []

        for function_call in function_calls:
            # use function_call_id as event_id
            function_call_id = function_call["id"]
            event_id = function_call_id

            tool_name = function_call["name"]
            arguments = function_call.get("arguments") or {}

            if self.tool_use_count.get(tool_name) and not (round_index in self.tool_use_count[tool_name]):
                self.tool_use_count[tool_name].append(round_index)
                if len(self.tool_use_count[tool_name]) > self.max_tool_use_count:
                    self.chat_completion_functions = [
                        item for item in self.chat_completion_functions if item["name"] != tool_name
                    ]
                    raise MessageGenerationException(f"{tool_name} has been used for more than 5 rounds.")
            else:
                if tool_name in self.tool_dict or tool_name == self.retrieval_tool_name:
                    # ensure tool_name is in the tool dict, or it is the retrieval tool
                    self.tool_use_count[tool_name] = [round_index]
                else:
                    raise MessageGenerationException(
                        f"The tool {tool_name} called by the model {self.model.model_id} "
                        f"({self.model.provider_id}/{self.model.provider_model_id}) does not exist."
                    )

            if log:
                if tool_name == self.retrieval_tool_name:
                    # retrieval
                    query_text = arguments.get("query_text")
                    retrieval_input_log_dict = build_retrieval_input_log_dict(
                        session_id=self.session_id,
                        event_id=event_id,
                        query_text=query_text,
                        top_k=self.assistant.retrieval_configs.top_k,
                    )
                    logs.append(retrieval_input_log_dict)

                # yield before running the tool

        return logs

    async def run_tools(self, function_calls, log=False):
        """
        Run tool and optionally log the result.
        :param function_calls: function call dict received from chat completion
        :param log: whether to log the tool action result
        :return: generator of tool action result log dicts if log is True else None
        """
        # Append function_calls message
        self.chat_completion_messages.append({"role": "assistant", "function_calls": function_calls})

        tool_inputs = []

        for function_call in function_calls:
            function_call_id = function_call["id"]
            tool_name = function_call["name"]
            arguments = function_call.get("arguments") or {}

            if tool_name == self.retrieval_tool_name:
                # Retrieval
                query_text = arguments.get("query_text")
                if not query_text:
                    raise MessageGenerationException("Error occurred when retrieving related documents")

                retrieval_content, retrieval_results = await query_assistant_retrieval(
                    assistant=self.assistant,
                    query_text=query_text,
                )

                logger.debug(f"Retrieval query: {query_text}")
                logger.debug(f"Retrieval result: {str(retrieval_results)[:200]}...")

                # Logging for retrieval
                if log:
                    retrieval_output_log_dict = build_retrieval_output_log_dict(
                        session_id=self.session_id,
                        event_id=function_call_id,
                        retrieval_result=retrieval_results,
                    )
                    yield retrieval_output_log_dict

                # Append tool result message
                self.chat_completion_messages.append(
                    {"role": "function", "content": retrieval_content, "id": function_call_id}
                )

            else:
                tool_input = ToolInput(
                    type=self.tool_dict[tool_name].type,
                    tool_id=self.tool_dict[tool_name].tool_id,
                    tool_call_id=function_call_id,
                    arguments=arguments,
                )
                tool_inputs.append(tool_input)

        if tool_inputs:
            if log:
                for tool_input in tool_inputs:
                    tool_input_log_dict = build_tool_input_log_dict(
                        session_id=self.session_id,
                        event_id=tool_input.tool_call_id,
                        tool_input=tool_input,
                    )
                    yield tool_input_log_dict
            tool_outputs: List[ToolOutput] = await run_tools(tool_inputs)
            for tool_output in tool_outputs:
                self.chat_completion_messages.append(tool_output.to_function_message())

                # Logging for other tools
                if log:
                    tool_action_result_log_dict = build_tool_output_log_dict(
                        session_id=self.session_id,
                        event_id=tool_output.tool_call_id,
                        # tool_name=tool_output.tool_name,
                        tool_output=tool_output,
                    )
                    yield tool_action_result_log_dict

    async def inference(self):
        chat_completion_response = await chat_completion(
            model_schema_id=self.model.model_schema_id,
            provider_model_id=self.model.provider_model_id,
            messages=self.chat_completion_messages,
            encrypted_credentials=self.model.encrypted_credentials,
            properties=self.model.properties,
            configs={},
            function_call=None,  # todo
            functions=self.chat_completion_functions,
        )
        check_http_error(chat_completion_response)
        completion_data = chat_completion_response.json()["data"]
        assistant_message_dict = completion_data["message"]
        function_calls = assistant_message_dict.get("function_calls")
        return assistant_message_dict, function_calls
