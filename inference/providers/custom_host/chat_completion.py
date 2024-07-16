from app.models import ModelSchema
from provider_dependency.chat_completion import *
from .chat_completion_tool_calls import CustomHostToolCallsChatCompletionModel
from .chat_completion_function_call import CustomHostFunctionCallChatCompletionModel
from app.models.tokenizer import estimate_input_tokens
from app.models import ProviderCredentials, ModelSchema
from .utils import *
from typing import Dict

logger = logging.getLogger(__name__)


class CustomHostChatCompletionModel(BaseChatCompletionModel):
    def __init__(self):
        self.openai_tool_calls_instance = CustomHostToolCallsChatCompletionModel()
        self.openai_function_call_instance = CustomHostFunctionCallChatCompletionModel()
        super().__init__()

    async def chat_completion(
        self,
        provider_model_id: str,
        messages: List[ChatCompletionMessage],
        credentials: ProviderCredentials,
        configs: ChatCompletionModelConfiguration,
        function_call: Optional[str] = None,
        functions: Optional[List[ChatCompletionFunction]] = None,
        proxy: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None,
        model_schema: ModelSchema = None,
    ):
        if provider_model_id == "openai-function-call":
            instance = self.openai_function_call_instance
        elif provider_model_id == "openai-tool-calls":
            instance = self.openai_tool_calls_instance
        else:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR,
                f"Provider model id only supports 'openai-function-call' and 'openai-tool-calls', but got {provider_model_id}",
            )
        model_id = credentials.CUSTOM_HOST_MODEL_ID
        # Convert ChatCompletionMessages to the required format
        api_url, headers, payload = await instance.prepare_request(
            False, model_id, messages, credentials, configs, function_call, functions, model_schema
        )

        for url in CONFIG.PROVIDER_URL_BLACK_LIST:
            if url in api_url:
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"Invalid provider url: {url}")
        input_tokens = estimate_input_tokens(
            [message.model_dump() for message in messages],
            [function.model_dump() for function in functions] if functions else None,
            function_call,
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                await self.handle_response(response)
                result = await response.json()
                core_data = instance.extract_core_data(result)
                text_content = instance.extract_text_content(core_data)
                function_calls = instance.extract_function_calls(core_data)
                finish_reason = instance.extract_finish_reason(core_data)
        response = self.prepare_response(
            finish_reason=finish_reason,
            text_content=text_content,
            function_calls_content=None,
            function_calls=function_calls,
            input_tokens=input_tokens,
            output_tokens=None,
        )
        return response

    # ------------------- chat completion stream -------------------

    async def chat_completion_stream(
        self,
        provider_model_id: str,
        messages: List[ChatCompletionMessage],
        credentials: ProviderCredentials,
        configs: ChatCompletionModelConfiguration,
        function_call: Optional[str] = None,
        functions: Optional[List[ChatCompletionFunction]] = None,
        proxy: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None,
        model_schema: ModelSchema = None,
    ):
        if provider_model_id == "openai-function-call":
            instance = self.openai_function_call_instance
        elif provider_model_id == "openai-tool-calls":
            instance = self.openai_tool_calls_instance
        else:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR,
                f"Provider model id only supports 'openai-function-call' and 'openai-tool-calls', but got {provider_model_id}",
            )
        model_id = credentials.CUSTOM_HOST_MODEL_ID
        api_url, headers, payload = await instance.prepare_request(
            True, model_id, messages, credentials, configs, function_call, functions, model_schema
        )

        input_tokens = estimate_input_tokens(
            [message.model_dump() for message in messages],
            [function.model_dump() for function in functions] if functions else None,
            function_call,
        )

        index = 0
        text_content = ""
        finish_reason = ChatCompletionFinishReason.unknown
        function_calls_content = ChatCompletionFunctionCallsContent()

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                await self.handle_response(response)
                async_stream_generator = response.content
                async_stream = AsyncStream(async_stream_generator)

                async for data in async_stream:
                    instance.stream_check_error(data)

                    # the main chunk data
                    chunk_data = instance.stream_extract_chunk_data(data)

                    # chunk
                    index, chunk = instance.stream_extract_chunk(index, chunk_data, text_content)
                    if chunk:
                        yield chunk
                        text_content += chunk.delta

                    # function call
                    _function_calls_content = instance.stream_handle_function_calls(chunk_data, function_calls_content)
                    if _function_calls_content:
                        function_calls_content = _function_calls_content

                    finish_reason = instance.stream_extract_finish_reason(chunk_data)

                response = self.prepare_response(
                    finish_reason=finish_reason,
                    text_content=text_content,
                    function_calls_content=function_calls_content,
                    function_calls=None,
                    input_tokens=input_tokens,
                    output_tokens=None,
                )
                yield response
