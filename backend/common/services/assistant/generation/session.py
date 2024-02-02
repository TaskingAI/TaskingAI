import json
from abc import ABC
from .utils import *
from .log import *
from common.models import MessageRole, MessageContent, Model, ModelSchema, Assistant, Chat
from common.services.assistant.message import create_message
from common.services.model.model import get_model
from common.services.assistant.assistant import get_assistant
from common.services.assistant.chat import get_chat
from common.services.tool.action import run_action
from common.services.inference.chat_completion import chat_completion
from common.utils import check_http_error
from common.error import ErrorCode, raise_http_error
import logging

logger = logging.getLogger(__name__)


class Session(ABC):
    def __init__(self, assistant_id, chat_id):
        # assistant
        self.assistant: Assistant = None

        # chat
        self.chat: Chat = None

        # tools
        self.tool_dict = None
        self.tool_use_count = {}
        self.max_tool_use_count = 5
        # todo config this in tools

        # retrievals
        self.retrieval_tool_name = None
        self.retrieval_collection_ids = None

        # model
        self.model: Model = None
        self.model_schema: ModelSchema = None

        # chat memory
        # self.chat_memory_context_summary = None
        self.chat_memory_messages = None

        # chat completion parameters
        self.system_prompt = None
        self.chat_completion_messages = None
        self.chat_completion_functions = None

        # ids
        self.assistant_id = assistant_id
        self.chat_id = chat_id
        self.session_id = generate_random_session_id()

        self.prepare_logs = []

    async def create_assistant_message(self, content_text: str):
        return await create_message(
            assistant_id=self.assistant_id,
            chat_id=self.chat_id,
            role=MessageRole.ASSISTANT,
            content=MessageContent(text=content_text),
            metadata={},
        )

    async def prepare(self, stream: bool, system_prompt_variables: Dict, retrival_log: bool = False):
        # 1. Get assistant
        self.assistant = await get_assistant(self.assistant_id)

        # 2. Get chat
        self.chat = await get_chat(self.assistant_id, self.chat_id)

        # 3. Get model
        self.model = await get_model(self.assistant.model_id)
        self.model_schema = self.model.model_schema()

        model_streaming: bool = self.model.properties.get("streaming", False)
        if not model_streaming and stream:
            raise_http_error(
                ErrorCode.INVALID_REQUEST,
                message=f"Assistant model {self.model.model_id} does not support streaming. "
                f"Please disable stream in the request.",
            )

        # 4. Get chat memory
        self.chat_memory_messages = await get_chat_memory_messages(self.assistant_id, self.chat_id)
        logger.debug(f"Chat memory: {self.chat_memory_messages}")

        # 5. Get tools
        self.tool_use_count = {}
        self.tool_dict, self.chat_completion_functions = await fetch_tool_functions(self.assistant.tools)
        logger.debug(f"Tool functions fetched: {self.chat_completion_functions}")

        # 6. Get retrievals
        retrieval_doc = None

        if self.assistant.retrievals:
            self.retrieval_collection_ids = [
                retrieval.id for retrieval in self.assistant.retrievals if retrieval.type == "collection"
            ]

            if self.assistant.retrieval_configs.method != AssistantRetrievalMethod.FUNCTION_CALL:
                # build query text and query retrieval collections
                retrieval_query_text = get_system_prompt_retrieval_query_text(
                    chat_memory_messages=self.chat_memory_messages,
                    method=self.assistant.retrieval_configs.method,
                )
                if retrieval_query_text:
                    retrieval_event_id = generate_random_event_id()
                    if retrival_log:
                        retrieval_log_input = build_retrieval_collection_input_log_dict(
                            session_id=self.session_id,
                            event_id=retrieval_event_id,
                            collection_ids=self.retrieval_collection_ids,
                            query_text=retrieval_query_text,
                            top_k=self.assistant.retrieval_configs.top_k,
                        )
                        self.prepare_logs.append(retrieval_log_input)

                    retrieval_doc, retrieval_chunks = await query_retrieval_collections(
                        collection_ids=self.retrieval_collection_ids,
                        query_text=retrieval_query_text,
                        top_k=self.assistant.retrieval_configs.top_k,
                    )

                    if retrival_log:
                        retrieval_log_output = build_retrieval_collection_output_log_dict(
                            session_id=self.session_id,
                            event_id=retrieval_event_id,
                            collection_ids=self.retrieval_collection_ids,
                            chunks=retrieval_chunks,
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

            if self.tool_use_count.get(tool_name) and not (round in self.tool_use_count[tool_name]):
                self.tool_use_count[tool_name].append(round)
                if len(self.tool_use_count[tool_name]) > self.max_tool_use_count:
                    self.chat_completion_functions = [
                        item for item in self.chat_completion_functions if item["name"] != tool_name
                    ]
                    raise MessageGenerationException(f"{tool_name} has been used for more than 5 rounds.")
            else:
                if tool_name in self.tool_dict:
                    # ensure tool_name is in the tool dict
                    self.tool_use_count[tool_name] = [round]
                else:
                    raise MessageGenerationException(
                        f"The tool {tool_name} called by the model {self.model_schema.model_id} "
                        f"({self.model_schema.provider_id}/{self.model_schema.provider_model_id}) does not exist."
                    )

            if log:
                if tool_name == self.retrieval_tool_name:
                    # retrieval
                    query_text = arguments.get("query_text")
                    retrieval_input_log_dict = build_retrieval_collection_input_log_dict(
                        session_id=self.session_id,
                        event_id=event_id,
                        collection_ids=self.retrieval_collection_ids,
                        query_text=query_text,
                        top_k=self.assistant.retrieval_configs.top_k,
                    )
                    logs.append(retrieval_input_log_dict)

                else:
                    tool_id = self.tool_dict[tool_name]["id"]
                    tool_action_call_log_dict = build_tool_action_input_log_dict(
                        session_id=self.session_id,
                        event_id=event_id,
                        action_id=tool_id,
                        name=tool_name,
                        arguments=arguments,
                    )
                    logs.append(tool_action_call_log_dict)

        return logs

    async def run_tools_without_log(self, function_calls):
        """
        run tool and log the result
        :param function_calls: function call dict received from chat completion
        :param log: whether to log the tool action result
        :return: tool action result log dict if log is True else None
        """

        # append function_calls message
        self.chat_completion_messages.append({"role": "assistant", "function_calls": function_calls})

        for function_call in function_calls:
            function_call_id = function_call["id"]
            tool_name = function_call["name"]
            arguments = function_call.get("arguments") or {}

            if tool_name == self.retrieval_tool_name:
                logger.debug(f"Use function call retrieval!\n" + "-" * 30)

                # retrieval
                query_text = arguments.get("query_text")
                if not query_text:
                    raise MessageGenerationException("Error occurred when retrieving related documents")

                logger.debug(f"Query text: {query_text}")
                tool_result, _ = await query_retrieval_collections(
                    collection_ids=self.retrieval_collection_ids,
                    query_text=query_text,
                    top_k=self.assistant.retrieval_configs.top_k,
                )
                logger.debug(f"Retrieval result: {query_text}" + "\n" + "-" * 30)

            else:
                tool_type = self.tool_dict[tool_name]["type"]
                tool_id = self.tool_dict[tool_name]["id"]

                if tool_type == "action":
                    tool_result_dict = await run_action(
                        action_id=tool_id,
                        parameters=arguments,
                        headers={},
                    )
                    tool_result = json.dumps(tool_result_dict)
                    logger.debug(f"Action result: {tool_result}")

                else:
                    # todo handle other tool types
                    raise NotImplementedError

            # append tool result message
            self.chat_completion_messages.append({"role": "function", "content": tool_result, "id": function_call_id})

    async def run_tools_with_log(self, function_calls):
        """
        run tool and log the result
        :param function_calls: function call dict received from chat completion
        :param log: whether to log the tool action result
        :return: tool action result log dict if log is True else None
        """

        # append function_calls message
        self.chat_completion_messages.append({"role": "assistant", "function_calls": function_calls})

        for function_call in function_calls:
            function_call_id = function_call["id"]
            event_id = function_call_id

            tool_name = function_call["name"]
            arguments = function_call.get("arguments") or {}

            if tool_name == self.retrieval_tool_name:
                logger.debug(f"Use function call retrieval!\n" + "-" * 30)

                # retrieval
                query_text = arguments.get("query_text")
                if not query_text:
                    raise MessageGenerationException("Error occurred when retrieving related documents")

                logger.debug(f"Query text: {query_text}")
                tool_result, related_chunks = await query_retrieval_collections(
                    collection_ids=self.retrieval_collection_ids,
                    query_text=query_text,
                    top_k=self.assistant.retrieval_configs.top_k,
                )
                logger.debug(f"Retrieval result: {query_text}" + "\n" + "-" * 30)

                retrieval_output_log_dict = build_retrieval_collection_output_log_dict(
                    session_id=self.session_id,
                    event_id=event_id,
                    collection_ids=self.retrieval_collection_ids,
                    chunks=related_chunks,
                )
                yield retrieval_output_log_dict

            else:
                tool_type = self.tool_dict[tool_name]["type"]
                tool_id = self.tool_dict[tool_name]["id"]

                if tool_type == "action":
                    tool_result_dict = await run_action(
                        action_id=tool_id,
                        parameters=arguments,
                        headers={},
                    )
                    tool_result = json.dumps(tool_result_dict)
                    logger.debug(f"Action result: {tool_result}")

                    tool_action_result_log_dict = build_tool_action_output_log_dict(
                        session_id=self.session_id,
                        event_id=event_id,
                        action_id=tool_id,
                        name=tool_name,
                        output=tool_result_dict,
                    )
                    yield tool_action_result_log_dict

                else:
                    # todo handle other tool types
                    raise NotImplementedError

            # append tool result message
            self.chat_completion_messages.append({"role": "function", "content": tool_result, "id": function_call_id})

    async def inference(self):
        chat_completion_response = await chat_completion(
            provider_id=self.model_schema.provider_id,
            provider_model_id=self.model_schema.provider_model_id,
            messages=self.chat_completion_messages,
            encrypted_credentials=self.model.encrypted_credentials,
            configs={},
            function_call=None,  # todo
            functions=self.chat_completion_functions,
        )
        check_http_error(chat_completion_response)
        completion_data = chat_completion_response.json()["data"]
        assistant_message_dict = completion_data["message"]
        function_calls = assistant_message_dict.get("function_calls")
        return assistant_message_dict, function_calls
