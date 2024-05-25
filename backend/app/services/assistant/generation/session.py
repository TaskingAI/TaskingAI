import logging
from fastapi import HTTPException
from abc import ABC
from typing import Dict, List, Optional, Tuple

from app.models import (
    MessageRole,
    MessageContent,
    Model,
    Assistant,
    Chat,
    Tool,
    ToolInput,
    ToolOutput,
    ChatCompletionAnyMessage,
    ChatCompletionFunction,
    ChatCompletionRole,
    RetrievalMethod,
)

from app.operators import message_ops
from app.services.model import get_model
from app.services.tool import run_tools, fetch_tools
from app.services.inference.chat_completion import chat_completion, stream_chat_completion

from .utils import *
from .log import *

logger = logging.getLogger(__name__)

__all__ = ["Session", "MESSAGE_CHUNK", "MESSAGE", "USAGE", "MESSAGE_RESPONSE"]

MESSAGE_CHUNK = 2
MESSAGE = 3
USAGE = 4
MESSAGE_RESPONSE = 5


class Session(ABC):
    def __init__(self, assistant: Assistant, chat: Optional[Chat], save_logs: bool):
        # assistant
        self.assistant: Assistant = assistant
        self.chat: Optional[Chat] = chat

        # tools
        self.tool_dict: Dict[str, Tool] = {}
        self.tool_use_count: Dict[str, List[int]] = {}
        self.max_tool_use_count = 5

        # functions (input by stateless chat completion)
        self.function_names = []

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

        # usage
        self.total_input_tokens = 0
        self.total_output_tokens = 0

        # logs
        self.logs = []
        self.save_logs = save_logs

    async def create_assistant_message(self, content_text: str, logs: List[Dict] = None):
        if not self.chat:
            raise MessageGenerationInvalidRequestException("Chat is required to create a message.")
        return await message_ops.create(
            assistant_id=self.assistant.assistant_id,
            chat_id=self.chat.chat_id,
            create_dict={
                "role": MessageRole.ASSISTANT.value,
                "content": MessageContent(text=content_text),
                "metadata": {},
                "logs": logs,
            },
            check_max_count=False,
        )

    async def prepare(
        self,
        stream: bool,
        system_prompt_variables: Dict,
        retrieval_log: bool = False,
        chat_completion_messages: List[ChatCompletionAnyMessage] = None,
        chat_completion_input_functions: List[ChatCompletionFunction] = None,
    ):
        """
        Prepare the session for generating messages.
        :param stream: whether to enable streaming
        :param system_prompt_variables: system prompt variables
        :param retrieval_log: whether to log retrieval
        :param chat_completion_messages: chat completion messages
        :param chat_completion_input_functions: chat completion input functions
        :return: None
        """

        if self.chat and chat_completion_messages is not None:
            raise ValueError("chat_completion_messages should be None when chat is not None.")

        if not self.chat and chat_completion_messages is None:
            raise ValueError("chat_completion_messages should not be None when chat is None.")

        if chat_completion_input_functions is not None and chat_completion_messages is None:
            raise ValueError("chat_completion_input_functions should be None when chat_completion_messages is None.")

        # check chat lock
        if self.chat and await self.chat.is_chat_locked():
            raise MessageGenerationInvalidRequestException(
                f"Chat {self.chat.chat_id} is locked. Please try again later."
            )

        # Get model
        try:
            self.model = await get_model(self.assistant.model_id)
        except Exception as e:
            raise MessageGenerationInvalidRequestException(f"Failed to load model {self.assistant.model_id}.")

        # Check model streaming
        if not self.model.allow_streaming() and stream:
            raise MessageGenerationInvalidRequestException(
                f"Assistant model {self.model.model_id} does not support streaming. "
            )

        # Get chat memory
        if self.chat:
            self.chat_memory_messages = await get_chat_memory_messages(self.chat)
            logger.debug(f"Chat memory: {self.chat_memory_messages}")
        else:
            # use user input message as chat memory
            self.chat_memory_messages = [
                message.model_dump()
                for message in chat_completion_messages
                if message.role != ChatCompletionRole.SYSTEM
            ]

        # Get tools
        if self.assistant.tools:
            try:
                tools = await fetch_tools(self.assistant.tools)
            except HTTPException as e:
                raise MessageGenerationInvalidRequestException(f"Failed to fetch all the assistant tools: {e.detail}")
            self.tool_dict.update({tool.function_name(): tool for tool in tools})
            self.chat_completion_functions = [tool.function_def for tool in tools]
            logger.debug(f"Tool functions fetched: {self.chat_completion_functions}")

        if chat_completion_input_functions:
            self.chat_completion_functions.extend(
                [function.model_dump() for function in chat_completion_input_functions]
            )
            self.function_names = [function.name for function in chat_completion_input_functions]

        # Get retrievals
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
                        self.logs.append(retrieval_log_input)

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
                        self.logs.append(retrieval_log_output)

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

        if chat_completion_messages:
            user_system_prompt = [
                message.content for message in chat_completion_messages if message.role == ChatCompletionRole.SYSTEM
            ]
            if user_system_prompt:
                user_system_prompt = user_system_prompt[0]
                if "{{user_system_prompt}}" in self.system_prompt:
                    self.system_prompt = self.system_prompt.replace("{{user_system_prompt}}", user_system_prompt)
                else:
                    self.system_prompt += "\n\n" + user_system_prompt

            # todo write docs for this

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

        if self.save_logs:
            self.logs.extend(logs)
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
                    if self.save_logs:
                        self.logs.append(retrieval_output_log_dict)
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
                    if self.save_logs:
                        self.logs.append(tool_input_log_dict)
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
                    if self.save_logs:
                        self.logs.append(tool_action_result_log_dict)
                    yield tool_action_result_log_dict

    async def inference(self) -> Tuple[Dict, List, Dict, Dict]:
        """
        Perform chat completion inference
        :return: a tuple of assistant message dict, function calls dict, usage dict, and completion data dict
        """

        completion_data = await chat_completion(
            model=self.model,
            messages=self.chat_completion_messages,
            functions=self.chat_completion_functions,
            configs={},
        )

        assistant_message_dict = completion_data["message"]
        function_calls = assistant_message_dict.get("function_calls")
        usage = completion_data.get("usage")
        self.total_input_tokens += usage.get("input_tokens", 0)
        self.total_output_tokens += usage.get("output_tokens", 0)
        return assistant_message_dict, function_calls, usage, completion_data

    async def stream_inference(self, message_chunk_object_name="MessageChunk"):
        try:
            chunk_generator = await stream_chat_completion(
                model=self.model,
                messages=self.chat_completion_messages,
                functions=self.chat_completion_functions,
                configs={},
                chunk_handler=None,
            )
        except HTTPException as e:
            logger.error(f"HTTPException occurred in streaming chat completion: {e}")
            raise MessageGenerationException(f"Error occurred in streaming chat completion.")

        async for chunk in chunk_generator:
            if chunk.get("object").lower() == "error":
                raise MessageGenerationException(f"{chunk.get('message')}")

            assistant_message_dict = chunk.get("message")
            if assistant_message_dict:
                yield MESSAGE, assistant_message_dict
                usage = chunk.get("usage")
                if usage:
                    self.total_input_tokens += usage.get("input_tokens", 0)
                    self.total_output_tokens += usage.get("output_tokens", 0)
                    yield USAGE, usage
                yield MESSAGE_RESPONSE, chunk

            else:
                delta = chunk.get("delta")
                if delta:
                    chunk.update({"object": message_chunk_object_name})
                    yield MESSAGE_CHUNK, chunk

    def has_user_input_function_call(self, function_calls):
        """
        Check if the function calls contain user input function call
        :param function_calls: function calls
        :return: True if the function calls contain user input function call, else False
        """

        if not function_calls:
            return False
        for function_call in function_calls:
            if function_call["name"] in self.function_names:
                return True
        return False

    def filter_user_function_calls(self, function_calls) -> Optional[List[Dict]]:
        """
        Filter out the function calls that are not user input functions
        :param function_calls: the function calls in response assistant message
        :return: list of function calls that are user input functions if any, else None
        """

        results = [function_call for function_call in function_calls if function_call["name"] in self.function_names]

        if results:
            return results

        else:
            return None
