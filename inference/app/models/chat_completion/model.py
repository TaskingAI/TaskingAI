from abc import ABC
from typing import Dict, List, Optional, Tuple
from app.models import ProviderCredentials, ModelSchema
from .chat_completion import *
from .function_call import *
from .model_config import *
from app.error import raise_provider_api_error, raise_http_error, ErrorCode
from ..utils import generate_random_id
from .stream import AsyncStream
from ..tokenizer import *
from app.utils import get_current_timestamp_int
import json
import aiohttp
from config import CONFIG

import logging

logger = logging.getLogger(__name__)

__all__ = [
    "BaseChatCompletionModel",
    "ChatCompletionFunctionCallsContent",
    "build_function_call",
    "generate_random_function_call_id",
]


class ChatCompletionFunctionCallsContent(object):
    def __init__(self):
        # The index of the function call
        self.index: int = -1

        # The arguments of the function call
        self.arguments_strs: List[str] = []

        # The arguments of the function call
        self.arguments_dicts: List[Dict] = []

        # The names of the function call
        self.names: List[str] = []


def generate_random_function_call_id():
    """
    Generate a random function call ID.
    :return: The random function call ID.
    """
    return "P3lf" + generate_random_id(20)


def build_function_call(
    name: str,
    arguments_str: str = None,
    arguments_dict: Dict = None,
) -> ChatCompletionFunctionCall:
    """
    Build a function call from the name and arguments.
    """
    arguments_dicts = {}
    error_msg = "Failed to parse the function call arguments due to invalid JSON format or length limit"
    if arguments_dict:
        arguments_dicts = arguments_dict
    else:
        if arguments_str == "" or arguments_str is None:
            raise_provider_api_error(error_msg)
        try:
            arguments_dicts = json.loads(arguments_str)
        except json.decoder.JSONDecodeError:
            raise_provider_api_error(error_msg)
    return ChatCompletionFunctionCall(
        id=generate_random_function_call_id(),
        name=name,
        arguments=arguments_dicts,
    )


class BaseChatCompletionModel(ABC):
    def __init__(self):
        pass

    # ------------------- chat completion -------------------

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
        # Convert ChatCompletionMessages to the required format
        api_url, headers, payload = await self.prepare_request(
            False, provider_model_id, messages, credentials, configs, function_call, functions, model_schema
        )
        if proxy:
            if not proxy.startswith("https://"):
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid proxy URL. Must start with https://")
            # complete the proxy if not end with /
            api_url = proxy

        if custom_headers:
            headers.update(custom_headers)
        from app.cache import get_provider

        provider = get_provider(model_schema.provider_id)
        if not provider.return_token_usage:
            input_tokens = estimate_input_tokens(
                [message.model_dump() for message in messages],
                [function.model_dump() for function in functions] if functions else None,
                function_call,
            )
            output_tokens = None
        else:
            input_tokens = None
            output_tokens = None

        async with aiohttp.ClientSession() as session:
            logger.debug(f"api_url: {api_url}")
            logger.debug(f"headers: {headers}")
            async with session.post(api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                await self.handle_response(response)
                result = await response.json()
                core_data = self.extract_core_data(result)
                if provider.return_token_usage:
                    input_tokens, output_tokens = self.extract_usage_data(result)
                if core_data is None:
                    raise_provider_api_error(f"The model did not return a valid response. data: {result}")
                text_content = self.extract_text_content(core_data)
                function_calls = self.extract_function_calls(core_data)
                finish_reason = self.extract_finish_reason(core_data)
        response = self.prepare_response(
            finish_reason=finish_reason,
            text_content=text_content,
            function_calls_content=None,
            function_calls=function_calls,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
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
        api_url, headers, payload = await self.prepare_request(
            True, provider_model_id, messages, credentials, configs, function_call, functions, model_schema
        )
        if proxy:
            if not proxy.startswith("https://"):
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid proxy URL. Must start with https://")
            # complete the proxy if not end with /
            api_url = proxy

        if custom_headers:
            headers.update(custom_headers)
        from app.cache import get_provider

        provider = get_provider(model_schema.provider_id)
        if not provider.return_stream_token_usage:
            input_tokens = estimate_input_tokens(
                [message.model_dump() for message in messages],
                [function.model_dump() for function in functions] if functions else None,
                function_call,
            )
            output_tokens = None
        else:
            input_tokens = None
            output_tokens = None

        index = 0
        text_content = ""
        finish_reason = ChatCompletionFinishReason.unknown
        function_calls_content = ChatCompletionFunctionCallsContent()

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                await self.handle_response(response)
                async_stream_generator = response.content
                async_stream = AsyncStream(async_stream_generator)

                empty_stream = True
                async for data in async_stream:
                    self.stream_check_error(data)
                    if provider.return_stream_token_usage:
                        input_tokens, output_tokens = self.stream_extract_usage_data(data, input_tokens, output_tokens)

                    # the main chunk data
                    chunk_data = self.stream_extract_chunk_data(data)
                    if chunk_data is None:
                        continue
                    empty_stream = False

                    # chunk
                    index, chunk = self.stream_extract_chunk(index, chunk_data, text_content)
                    if chunk:
                        yield chunk
                        text_content += chunk.delta

                    # function call
                    _function_calls_content = self.stream_handle_function_calls(chunk_data, function_calls_content)
                    if _function_calls_content:
                        function_calls_content = _function_calls_content

                    finish_reason = self.stream_extract_finish_reason(chunk_data) or finish_reason

                if empty_stream:
                    raise_provider_api_error("The model stream response is empty.")

                response = self.prepare_response(
                    finish_reason=finish_reason,
                    text_content=text_content,
                    function_calls_content=function_calls_content,
                    function_calls=None,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                )
                yield response

    # ------------------- prepare request and response data -------------------

    async def prepare_request(
        self,
        stream: bool,
        provider_model_id: str,
        messages: List[ChatCompletionMessage],
        credentials: ProviderCredentials,
        configs: ChatCompletionModelConfiguration,
        function_call: Optional[str] = None,
        functions: Optional[List[ChatCompletionFunction]] = None,
        model_schema: ModelSchema = None,
    ) -> Tuple[str, Dict, Dict]:
        """
        Prepare the request for the chat completion model.
        :return: a tuple of the request url, headers, and body payload
        """
        raise NotImplementedError

    def prepare_response(
        self,
        finish_reason: ChatCompletionFinishReason,
        text_content: str,
        function_calls_content: Optional[ChatCompletionFunctionCallsContent],
        function_calls: Optional[List[ChatCompletionFunctionCall]],
        input_tokens: int = None,
        output_tokens: int = None,
    ) -> ChatCompletion:
        """
        Prepare the response from the chat completion model.
        :return: the assistant message.
        """
        message = None

        if text_content:
            text_content = text_content.strip()

        if function_calls:
            finish_reason = ChatCompletionFinishReason.function_calls
            message = ChatCompletionAssistantMessage(function_calls=function_calls)

        elif function_calls_content and function_calls_content.names:
            function_calls = []
            for i, name in enumerate(function_calls_content.names):
                strs = function_calls_content.arguments_strs
                dicts = function_calls_content.arguments_dicts
                function_call = build_function_call(
                    name=name,
                    arguments_str=strs[i] if strs else None,
                    arguments_dict=dicts[i] if dicts else None,
                )
                function_calls.append(function_call)
            finish_reason = ChatCompletionFinishReason.function_calls
            message = ChatCompletionAssistantMessage(function_calls=function_calls)

        else:
            if text_content is None:
                raise_provider_api_error("The model response is empty.")
            message = ChatCompletionAssistantMessage(content=text_content or "")

        if output_tokens is None:
            output_tokens = estimate_response_tokens(message.model_dump())
        usage = ChatCompletionUsage(input_tokens=input_tokens, output_tokens=output_tokens)
        response = ChatCompletion(
            created_timestamp=get_current_timestamp_int(),
            finish_reason=finish_reason,
            message=message,
            usage=usage,
        )
        return response

    @staticmethod
    async def handle_response(response):
        """
        Handles the HTTP response, raising specific errors based on the response status and error type.
        """
        if response.status >= 500:
            logger.error(f"response: {response}")
            raise_http_error(ErrorCode.PROVIDER_ERROR, "Provider's service is unavailable")
        if response.status != 200:
            try:
                result = await response.json()
            except Exception:
                result = await response.text()

            raise_provider_api_error(str(result))

    # ------------------- handle non-stream chat completion response -------------------

    def extract_core_data(self, response_data: Dict, **kwargs) -> Optional[Dict]:
        """
        :return: the message data extracted from the response data in non-streaming mode.
        """
        raise NotImplementedError

    def extract_text_content(self, data: Dict, **kwargs) -> Optional[str]:
        """
        :return: the message data extracted from the response data in non-streaming mode.
        """
        raise NotImplementedError

    def extract_function_calls(self, data: Dict, **kwargs) -> Optional[ChatCompletionFunctionCall]:
        """
        :return: the function calls delta extracted from the response data in non-streaming mode.
        """
        raise NotImplementedError

    def extract_finish_reason(self, data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        """
        :return: the finish reason extracted from the response data in non-streaming mode.
        """
        raise NotImplementedError

    # ------------------- handle stream chat completion response -------------------

    def stream_extract_chunk_data(self, sse_data: Dict, **kwargs) -> Optional[Dict]:
        """
        :return: the content data extracted from the sse data.
        """
        raise NotImplementedError

    def stream_check_error(self, sse_data: Dict, **kwargs):
        """
        Raise an error if the data contains an error.
        """
        raise NotImplementedError

    def stream_extract_chunk(
        self, index: int, chunk_data: Dict, text_content: str, **kwargs
    ) -> Tuple[int, Optional[ChatCompletionChunk]]:
        """
        :return: a tuple of the next index and the chunk extracted from the sse data.
        """
        raise NotImplementedError

    def stream_extract_messages(self, chunk_data: Dict, **kwargs) -> List[ChatCompletionMessage]:
        """
        :return: the messages extracted from the sse data.
        """
        raise NotImplementedError

    def stream_extract_finish_reason(self, chunk_data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        """
        :return: the finish reason extracted from the sse data.
        """
        raise NotImplementedError

    def stream_handle_function_calls(
        self, chunk_data: Dict, function_calls_content: ChatCompletionFunctionCallsContent, **kwargs
    ) -> Optional[ChatCompletionFunctionCallsContent]:
        """
        :return: the function calls delta extracted from the sse data.
        """
        raise NotImplementedError
