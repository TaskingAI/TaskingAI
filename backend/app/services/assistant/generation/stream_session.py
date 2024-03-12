import asyncio
import json
from .session import Session
from .utils import *
from .log import *
from .utils import generate_random_event_id
from app.services.inference.chat_completion import chat_completion_stream
from app.models import Assistant, Chat
from fastapi import HTTPException

import logging

logger = logging.getLogger(__name__)

MESSAGE_CHUNK = 2
MESSAGE = 3


def error_message(message: str):
    return {
        "object": "Error",
        "code": "GENERATION_ERROR",
        "message": message,
    }


class StreamSession(Session):
    def __init__(self, assistant: Assistant, chat: Chat, stream: bool, debug: bool):
        super().__init__(assistant, chat)
        self.stream = stream
        self.debug = debug

    async def stream_inference(self):
        async for temp_data in chat_completion_stream(
            model_schema_id=self.model.model_schema_id,
            provider_model_id=self.model.provider_model_id,
            messages=self.chat_completion_messages,
            encrypted_credentials=self.model.encrypted_credentials,
            properties=self.model.properties,
            configs={},
            function_call=None,  # todo
            functions=self.chat_completion_functions,
        ):
            if temp_data.get("object") == "Error":
                raise MessageGenerationException(f"{temp_data.get('message')}")
            assistant_message_dict = temp_data.get("message")
            if assistant_message_dict:
                yield MESSAGE, assistant_message_dict
            else:
                delta = temp_data.get("delta")
                if delta:
                    temp_data.update({"object": "MessageChunk"})
                    yield MESSAGE_CHUNK, temp_data

    async def stream_generate(self, system_prompt_variables: Dict):
        try:
            await self.prepare(self.stream, system_prompt_variables, retrieval_log=self.debug)
            await self.chat.lock()

            if self.prepare_logs:
                for log_dict in self.prepare_logs:
                    yield f"data: {json.dumps(log_dict)}\n\n"
                    await asyncio.sleep(0.1)

            function_calls_round_index = 0
            while True:
                chat_completion_function_calls_dict_list = None
                chat_completion_assistant_message_dict = None

                try:
                    chat_completion_event_id = generate_random_event_id()
                    if self.debug:
                        chat_completion_input_log_dict = build_chat_completion_input_log_dict(
                            session_id=self.session_id,
                            event_id=chat_completion_event_id,
                            model=self.model,
                            messages=self.chat_completion_messages,
                            functions=self.chat_completion_functions,
                        )
                        yield f"data: {json.dumps(chat_completion_input_log_dict)}\n\n"

                    if self.stream:
                        logger.debug(f"completion start inference, stream = {self.stream}")
                        async for t, data in self.stream_inference():
                            logger.debug(f"completion streaming, {t}: {data}")
                            if t == MESSAGE_CHUNK:
                                yield f"data: {json.dumps(data)}\n\n"
                            elif t == MESSAGE:
                                chat_completion_assistant_message_dict = data
                                function_calls = data.get("function_calls")
                                if function_calls:
                                    chat_completion_function_calls_dict_list = function_calls
                            else:
                                raise MessageGenerationException("Unknown data type")
                    else:
                        logger.debug(f"completion start inference, stream = {self.stream}")
                        (
                            chat_completion_assistant_message_dict,
                            chat_completion_function_calls_dict_list,
                        ) = await self.inference()

                    if self.debug:
                        chat_completion_output_log_dict = build_chat_completion_output_log_dict(
                            session_id=self.session_id,
                            event_id=chat_completion_event_id,
                            model=self.model,
                            message=chat_completion_assistant_message_dict,
                        )
                        yield f"data: {json.dumps(chat_completion_output_log_dict)}\n\n"

                except MessageGenerationException as e:
                    raise e
                except HTTPException as e:
                    raise MessageGenerationException(f"Error occurred in chat completion inference. {e.detail}")
                except Exception as e:
                    logger.error(f"Error occurred in chat completion inference: {e}")
                    raise MessageGenerationException(f"Error occurred in chat completion inference")

                if chat_completion_function_calls_dict_list:
                    function_calls_round_index += 1
                    try:
                        logger.debug(f"FUNCTION_CALLS: tool_call = {chat_completion_function_calls_dict_list}")

                        # use and run tool. When debug is True, log the tool action call and result
                        tool_action_call_logs = await self.use_tool(
                            function_calls=chat_completion_function_calls_dict_list,
                            round_index=function_calls_round_index,
                            log=self.debug,
                        )
                        if self.debug:
                            for tool_action_call_log_dict in tool_action_call_logs:
                                logger.debug(f"tool_action_call_log_dict = {tool_action_call_log_dict}")
                                yield f"data: {json.dumps(tool_action_call_log_dict)}\n\n"

                        # run tools

                        if self.debug:
                            async for tool_action_result_log_dict in self.run_tools(
                                function_calls=chat_completion_function_calls_dict_list, log=True
                            ):
                                logger.debug(f"tool_action_result_log_dict = {tool_action_result_log_dict}")
                                yield f"data: {json.dumps(tool_action_result_log_dict)}\n\n"
                        else:
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

            # raise MessageGenerationException("Manually raise error to test")
            message = await self.create_assistant_message(chat_completion_assistant_message_dict["content"])
            message_dict = message.to_response_dict()
            yield f"data: {json.dumps(message_dict)}\n\n"
            yield f"data: [DONE]\n\n"

        except MessageGenerationException as e:
            err_dict = error_message(str(e))
            yield f"data: {json.dumps(err_dict)}\n\n"
            yield f"data: [DONE]\n\n"

        except Exception as e:
            err_dict = error_message("Assistant message not generated due to an unknown error.")
            yield f"data: {json.dumps(err_dict)}\n\n"
            yield f"data: [DONE]\n\n"

        finally:
            await self.chat.unlock()
