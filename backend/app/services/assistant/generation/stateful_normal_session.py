from fastapi import HTTPException
from typing import Dict
from tkhelper.error import raise_http_error, ErrorCode
from tkhelper.schemas import BaseDataResponse
import logging

from app.models import Assistant, Chat

from .session import Session
from .utils import *
from .log import *

logger = logging.getLogger(__name__)


class StatefulNormalSession(Session):
    def __init__(self, assistant: Assistant, chat: Chat, save_logs: bool):
        super().__init__(assistant, chat, save_logs)

    async def generate(self, system_prompt_variables: Dict):
        try:
            await self.prepare(
                stream=False,
                system_prompt_variables=system_prompt_variables,
                retrieval_log=self.save_logs,
            )
            await self.chat.lock()

            function_calls_round_index = 0

            while True:
                try:
                    chat_completion_event_id = generate_random_event_id()
                    # append chat completion input log
                    if self.save_logs:
                        chat_completion_input_log_dict = build_chat_completion_input_log_dict(
                            session_id=self.session_id,
                            event_id=chat_completion_event_id,
                            model=self.model,
                            messages=self.chat_completion_messages,
                            functions=self.chat_completion_functions,
                        )
                        self.logs.append(chat_completion_input_log_dict)

                    # inference
                    (
                        chat_completion_assistant_message_dict,
                        chat_completion_function_calls_dict_list,
                        usage_dict,
                        _,
                    ) = await self.inference()

                    # append chat completion output log
                    if self.save_logs:
                        chat_completion_output_log_dict = build_chat_completion_output_log_dict(
                            session_id=self.session_id,
                            event_id=chat_completion_event_id,
                            model=self.model,
                            message=chat_completion_assistant_message_dict,
                            usage=usage_dict,
                        )
                        self.logs.append(chat_completion_output_log_dict)

                except HTTPException as e:
                    raise MessageGenerationException(f"Error occurred in chat completion inference. {e.detail}")
                except Exception as e:
                    raise MessageGenerationException(f"Error occurred in chat completion inference")

                logger.debug(f"chat_completion_assistant_message = {chat_completion_assistant_message_dict}")
                logger.debug(f"chat_completion_function_calls_dict_list = {chat_completion_function_calls_dict_list}")

                if chat_completion_function_calls_dict_list:
                    function_calls_round_index += 1
                    try:
                        await self.use_tool(
                            chat_completion_function_calls_dict_list,
                            round_index=function_calls_round_index,
                            log=self.save_logs,
                        )
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

            message = await self.create_assistant_message(
                content_text=chat_completion_assistant_message_dict["content"],
                logs=self.logs if self.save_logs else None,
            )
            return BaseDataResponse(data=message.to_response_dict())

        except MessageGenerationInvalidRequestException as e:
            logger.error(f"StatefulNormalSession.generate: HTTPException error = {e}")
            raise_http_error(ErrorCode.INVALID_REQUEST, message=str(e))

        except MessageGenerationException as e:
            logger.error(f"StatefulNormalSession.generate: MessageGenerationException error = {e}")
            raise_http_error(ErrorCode.GENERATION_ERROR, message=str(e))

        except Exception as e:
            logger.error(f"StatefulNormalSession.generate: Exception error = {e}")
            raise_http_error(
                ErrorCode.INTERNAL_SERVER_ERROR, message=str("Assistant message not generated due to an unknown error.")
            )

        finally:
            await self.chat.unlock()
