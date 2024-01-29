from .session import Session
from app.schemas.base import BaseSuccessDataResponse
from .utils import MessageGenerationException
from common.models import SerializePurpose
from common.error import raise_http_error, ErrorCode
from common.services.assistant.chat import unlock_chat
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


class NormalSession(Session):
    def __init__(self, assistant_id, chat_id):
        super().__init__(assistant_id, chat_id)

    async def generate(self):
        function_calls_round_index = 0

        try:
            while True:
                try:
                    chat_completion_assistant_message, chat_completion_function_calls_dict_list = await self.inference()
                except HTTPException as e:
                    raise MessageGenerationException(f"Error occurred in chat completion inference. {e.detail}")
                except Exception as e:
                    raise MessageGenerationException(f"Error occurred in chat completion inference")

                logger.debug(f"chat_completion_assistant_message = {chat_completion_assistant_message}")
                logger.debug(f"chat_completion_function_calls_dict_list = {chat_completion_function_calls_dict_list}")

                if chat_completion_function_calls_dict_list:
                    function_calls_round_index += 1
                    try:
                        await self.use_tool(
                            chat_completion_function_calls_dict_list, round_index=function_calls_round_index, log=False
                        )
                        await self.run_tools_without_log(chat_completion_function_calls_dict_list)
                    except MessageGenerationException as e:
                        logger.error(f"MessageGenerationException occurred in using the tools: {e}")
                        raise e
                    except Exception as e:
                        logger.error(f"MessageGenerationException occurred in using the tools: {e}")
                        raise MessageGenerationException(f"Error occurred in using the tools")

                else:
                    break

            message = await self.create_assistant_message(chat_completion_assistant_message["content"])
            return BaseSuccessDataResponse(data=message.to_dict(purpose=SerializePurpose.RESPONSE))

        except MessageGenerationException as e:
            logger.error(f"NormalSession.generate: MessageGenerationException error = {e}")
            raise_http_error(ErrorCode.INTERNAL_SERVER_ERROR, message=str(e))

        except Exception as e:
            logger.error(f"NormalSession.generate: Exception error = {e}")
            raise_http_error(
                ErrorCode.INTERNAL_SERVER_ERROR, message=str("Assistant message not generated due to an unknown error.")
            )

        finally:
            await unlock_chat(self.assistant_id, self.chat_id)
