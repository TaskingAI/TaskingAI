from .session import Session
from app.schemas.base import BaseSuccessDataResponse
from common.services.inference.chat_completion import chat_completion
from common.utils import check_http_error

import logging

logger = logging.getLogger(__name__)


class NormalSession(Session):
    def __init__(self, assistant_id, chat_id):
        super().__init__(assistant_id, chat_id)

    async def inference(self):
        chat_completion_response = await chat_completion(
            provider_id=self.model_schema.provider_id,
            provider_model_id=self.model_schema.provider_model_id,
            messages=self.chat_completion_messages,
            credentials=self.model.encrypted_credentials,
            configs={},
            function_call=None,  # todo
            functions=self.chat_completion_functions,
        )
        check_http_error(chat_completion_response)
        completion_data = chat_completion_response.json()["data"]
        assistant_message_dict = completion_data["message"]
        function_calls = assistant_message_dict.get("function_calls")
        return assistant_message_dict, function_calls

    async def generate(self):
        function_calls_round_index = 0

        # try:
        if 1:
            while True:
                # try:
                if 1:
                    chat_completion_assistant_message, chat_completion_function_calls_dict_list = await self.inference()
                # except Exception as e:
                #     raise MessageGenerationException(f"Error occurred in chat completion inference")

                logger.debug(f"chat_completion_assistant_message = {chat_completion_assistant_message}")
                logger.debug(f"chat_completion_function_calls_dict_list = {chat_completion_function_calls_dict_list}")

                if chat_completion_function_calls_dict_list:
                    function_calls_round_index += 1
                    # try:
                    if 1:
                        await self.use_tool(
                            chat_completion_function_calls_dict_list, round_index=function_calls_round_index, log=False
                        )
                        await self.run_tools_without_log(chat_completion_function_calls_dict_list)
                    # except MessageGenerationException as e:
                    #     logger.error(f"MessageGenerationException occurred in using the tools: {e}")
                    #     raise e
                    # except Exception as e:
                    #     logger.error(f"MessageGenerationException occurred in using the tools: {e}")
                    #     raise MessageGenerationException(f"Error occurred in using the tools")

                else:
                    break

            message = await self.create_assistant_message(chat_completion_assistant_message["content"])
            return BaseSuccessDataResponse(data=message.model_dump())

        # except MessageGenerationException as e:
        #     logger.error(f"NormalSession.generate: MessageGenerationException error = {e}")
        #     raise_http_error(ErrorCode.INTERNAL_SERVER_ERROR, message=str(e))
        #
        # except Exception as e:
        #     logger.error(f"NormalSession.generate: Exception error = {e}")
        #     raise_http_error(
        #         ErrorCode.INTERNAL_SERVER_ERROR, message=str("Assistant message not generated due to an unknown error.")
        #     )
        #
        # finally:
        #     await unlock_chat(self.assistant_id, self.chat_id)
