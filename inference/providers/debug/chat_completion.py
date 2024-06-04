from app.models import ModelSchema
from provider_dependency.chat_completion import *
from app.models.tokenizer import estimate_input_tokens, estimate_response_tokens
from typing import List, Dict, Optional
from app.models import ProviderCredentials, ModelSchema

logger = logging.getLogger(__name__)


def _build_debug_response(message: ChatCompletionMessage):
    if message.role == ChatCompletionRole.user:
        if isinstance(message.content, List):
            return str([c.model_dump() for c in message.content])
    return message.content


class DebugChatCompletionModel(BaseChatCompletionModel):
    def __init__(self):
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
        if provider_model_id == "debug-error" and messages[-1].content != "Only say your name":
            raise_http_error(ErrorCode.PROVIDER_ERROR, "Debug error for test")
        input_tokens = estimate_input_tokens(
            [message.model_dump() for message in messages],
            [function.model_dump() for function in functions] if functions else None,
            function_call,
        )

        finish_reason = ChatCompletionFinishReason.stop
        message_content = _build_debug_response(messages[-1])
        message_content = message_content[(len(message_content) // 2) :].strip()
        message = ChatCompletionAssistantMessage(content=message_content)
        output_tokens = estimate_response_tokens(message.model_dump())
        response = ChatCompletion(
            finish_reason=finish_reason,
            message=message,
            created_timestamp=get_current_timestamp_int(),
            usage=ChatCompletionUsage(input_tokens=input_tokens, output_tokens=output_tokens),
        )
        return response

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
        if not messages:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "No messages provided")

        if provider_model_id == "debug-error":
            raise_http_error(ErrorCode.PROVIDER_ERROR, "Debug error for test")

        input_tokens = estimate_input_tokens(
            [message.model_dump() for message in messages],
            [function.model_dump() for function in functions] if functions else None,
            function_call,
        )
        # Extract the last message
        message_content = _build_debug_response(messages[-1])
        message_content = message_content[(len(message_content) // 2) :].strip()
        # Split the message content into words
        words = message_content.split()

        # Simulate the streaming response by yielding each word
        for i, word in enumerate(words):
            yield ChatCompletionChunk(
                created_timestamp=get_current_timestamp_int(),
                index=i,
                delta=word,
            )
        message = ChatCompletionAssistantMessage(content=message_content)
        output_tokens = estimate_response_tokens(message.model_dump())
        finish_reason = ChatCompletionFinishReason.stop
        usage = ChatCompletionUsage(input_tokens=input_tokens, output_tokens=output_tokens)
        response = ChatCompletion(
            created_timestamp=get_current_timestamp_int(),
            finish_reason=finish_reason,
            message=message,
            usage=usage,
        )
        yield response
