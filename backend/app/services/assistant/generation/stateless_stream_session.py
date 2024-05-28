import json
from typing import List, Union
from fastapi import HTTPException

from tkhelper.utils import SSE_DONE_MSG
from tkhelper.error import ErrorCode

from app.models.inference import *
from app.models import Assistant

from .session import *
from .utils import *
from .log import *
from .utils import generate_random_event_id

import logging

logger = logging.getLogger(__name__)


def error_message(code, message: str):
    return {
        "object": "Error",
        "code": code,
        "message": message,
    }


class StatelessStreamSession(Session):
    def __init__(self, assistant: Assistant, save_logs: bool, yield_dict: bool = False):
        super().__init__(assistant, None, save_logs)
        self.stream = True
        self.yield_dict = yield_dict

    async def stream_generate(
        self,
        messages: List[
            Union[
                ChatCompletionFunctionMessage,
                ChatCompletionAssistantMessage,
                ChatCompletionUserMessage,
                ChatCompletionSystemMessage,
            ]
        ],
        functions: List[ChatCompletionFunction],
    ):
        response_dict = None

        try:
            await self.prepare(
                stream=self.stream,
                system_prompt_variables={},
                retrieval_log=self.save_logs,
                chat_completion_messages=messages,
                chat_completion_input_functions=functions,
            )

            function_calls_round_index = 0
            while True:
                chat_completion_function_calls_dict_list = None
                chat_completion_assistant_message_dict = None

                try:
                    chat_completion_event_id = generate_random_event_id()
                    if self.save_logs:
                        chat_completion_input_log_dict = build_chat_completion_input_log_dict(
                            session_id=self.session_id,
                            event_id=chat_completion_event_id,
                            model=self.model,
                            messages=self.chat_completion_messages,
                            functions=self.chat_completion_functions,
                        )
                        if self.save_logs:
                            self.logs.append(chat_completion_input_log_dict)

                    if self.stream:
                        usage_dict = None
                        logger.debug(f"completion start inference, stream = {self.stream}")
                        async for t, data in self.stream_inference(message_chunk_object_name="ChatCompletionChunk"):
                            logger.debug(f"completion streaming, {t}: {data}")
                            if t == MESSAGE_CHUNK:
                                if self.yield_dict:
                                    yield data
                                else:
                                    yield f"data: {json.dumps(data)}\n\n"
                            elif t == MESSAGE:
                                chat_completion_assistant_message_dict = data
                                function_calls = data.get("function_calls")
                                if function_calls:
                                    chat_completion_function_calls_dict_list = function_calls
                            elif t == USAGE:
                                usage_dict = data
                            elif t == MESSAGE_RESPONSE:
                                response_dict = data
                            else:
                                raise MessageGenerationException("Unknown data type")
                    else:
                        logger.debug(f"completion start inference, stream = {self.stream}")
                        (
                            chat_completion_assistant_message_dict,
                            chat_completion_function_calls_dict_list,
                            usage_dict,
                            response_dict,
                        ) = await self.inference()

                    if self.save_logs:
                        chat_completion_output_log_dict = build_chat_completion_output_log_dict(
                            session_id=self.session_id,
                            event_id=chat_completion_event_id,
                            model=self.model,
                            message=chat_completion_assistant_message_dict,
                            usage=usage_dict,
                        )
                        if self.save_logs:
                            self.logs.append(chat_completion_output_log_dict)

                except MessageGenerationException as e:
                    raise e
                except HTTPException as e:
                    logger.error(f"HTTPException occurred in chat completion inference: {e}")
                    raise MessageGenerationException(f"Error occurred in chat completion inference. {e.detail}")
                except Exception as e:
                    logger.error(f"Error occurred in chat completion inference: {e}")
                    raise MessageGenerationException(f"Error occurred in chat completion inference")

                if chat_completion_function_calls_dict_list:
                    # check if there are any user functions in the chat completion response
                    # if there are, filter them and return them in the response
                    # don't include other tool calls in the response
                    filtered_user_function_calls = self.filter_user_function_calls(
                        chat_completion_function_calls_dict_list
                    )
                    if filtered_user_function_calls:
                        response_dict["message"]["function_calls"] = filtered_user_function_calls
                        break

                    function_calls_round_index += 1
                    try:
                        logger.debug(f"FUNCTION_CALLS: tool_call = {chat_completion_function_calls_dict_list}")

                        # use and run tool. When debug is True, log the tool action call and result
                        tool_action_call_logs = await self.use_tool(
                            function_calls=chat_completion_function_calls_dict_list,
                            round_index=function_calls_round_index,
                            log=self.save_logs,
                        )
                        # run tools
                        async for _ in self.run_tools(chat_completion_function_calls_dict_list):
                            pass

                    except MessageGenerationException as e:
                        logger.error(f"MessageGenerationException occurred in using the tools: {e}")
                        raise e

                    except Exception as e:
                        logger.error(f"Error occurred in using the tools: {e}")
                        raise MessageGenerationException(f"Error occurred in using the tools")

                else:
                    break

            if not chat_completion_assistant_message_dict:
                raise MessageGenerationException("Assistant message not generated.")

            if not response_dict:
                raise MessageGenerationException("Assistant message not generated.")

            # raise MessageGenerationException("Manually raise error to test")
            response_dict["usage"]["input_tokens"] = self.total_input_tokens
            response_dict["usage"]["output_tokens"] = self.total_output_tokens
            if self.yield_dict:
                yield response_dict
            else:
                yield f"data: {json.dumps(response_dict)}\n\n"
                yield SSE_DONE_MSG

        except MessageGenerationInvalidRequestException as e:
            err_dict = error_message(code=ErrorCode.INVALID_REQUEST, message=str(e))
            if self.yield_dict:
                yield err_dict
            else:
                yield f"data: {json.dumps(err_dict)}\n\n"
                yield SSE_DONE_MSG

        except MessageGenerationException as e:
            err_dict = error_message(code=ErrorCode.GENERATION_ERROR, message=str(e))
            if self.yield_dict:
                yield err_dict
            else:
                yield f"data: {json.dumps(err_dict)}\n\n"
                yield SSE_DONE_MSG

        except Exception as e:
            err_dict = error_message(
                code=ErrorCode.UNKNOWN_ERROR,
                message="Assistant message not generated due to an unknown error.",
            )
            logger.error(f"stream_generate: unknown error occurred in stream_generate {e}")
            if self.yield_dict:
                yield err_dict
            else:
                yield f"data: {json.dumps(err_dict)}\n\n"
                yield SSE_DONE_MSG
