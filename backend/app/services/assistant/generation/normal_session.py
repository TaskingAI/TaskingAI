from fastapi import HTTPException
from typing import Dict
from tkhelper.error import raise_http_error, ErrorCode
from tkhelper.schemas import BaseDataResponse
import logging

from app.models import Assistant, Chat

from .session import Session
from .utils import MessageGenerationException

logger = logging.getLogger(__name__)


class NormalSession(Session):
    def __init__(self, assistant: Assistant, chat: Chat):
        super().__init__(assistant, chat)

    async def generate(self, system_prompt_variables: Dict):
        try:
            await self.prepare(False, system_prompt_variables, retrieval_log=False)
            await self.chat.lock()

            function_calls_round_index = 0

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
                        async for _ in self.run_tools(chat_completion_function_calls_dict_list):
                            pass
                    except MessageGenerationException as e:
                        logger.error(f"MessageGenerationException occurred in using the tools: {e}")
                        raise e
                    except Exception as e:
                        logger.error(f"MessageGenerationException occurred in using the tools: {e}")
                        raise MessageGenerationException(f"Error occurred in using the tools")

                else:
                    break

            message = await self.create_assistant_message(chat_completion_assistant_message["content"])
            return BaseDataResponse(data=message.to_response_dict())

        except MessageGenerationException as e:
            logger.error(f"NormalSession.generate: MessageGenerationException error = {e}")
            raise_http_error(ErrorCode.GENERATION_ERROR, message=str(e))

        except Exception as e:
            logger.error(f"NormalSession.generate: Exception error = {e}")
            raise_http_error(
                ErrorCode.INTERNAL_SERVER_ERROR, message=str("Assistant message not generated due to an unknown error.")
            )

        finally:
            await self.chat.unlock()
