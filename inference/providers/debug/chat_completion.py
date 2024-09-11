from app.models import ModelSchema
import copy
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


TOOL_CALL_HALLUCINATION_MESSAGE = ChatCompletionAssistantMessage(
    content=None,
    role=ChatCompletionRole.assistant,
    function_calls=[
        {
            "id": "P3lffDFvUpOJW3PxfB8ecoqw",
            "name": "make_scatter_plot",
            "arguments": {"x_values": [1, 2], "y_values": [3, 4]},
        }
    ],
)

ASSISTANT_CONTENT_DEBUG_MESSAGE = ChatCompletionAssistantMessage(
    content="Test Message",
    role=ChatCompletionRole.assistant,
)


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
        if provider_model_id == "debug-tool-call-hallucinations" and messages[-1].role == ChatCompletionRole.user:
            finish_reason = ChatCompletionFinishReason.function_calls
            message = copy.deepcopy(TOOL_CALL_HALLUCINATION_MESSAGE)
        elif provider_model_id == "debug-tool-call-hallucinations" and messages[-1].role == ChatCompletionRole.function:
            finish_reason = ChatCompletionFinishReason.stop
            message = copy.deepcopy(ASSISTANT_CONTENT_DEBUG_MESSAGE)
        else:
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

        if provider_model_id == "debug-tool-call-hallucinations" and messages[-1].role == ChatCompletionRole.user:
            output_message = copy.deepcopy(TOOL_CALL_HALLUCINATION_MESSAGE)
            finish_reason = ChatCompletionFinishReason.function_calls
        elif provider_model_id == "debug-tool-call-hallucinations" and messages[-1].role == ChatCompletionRole.function:
            output_message = copy.deepcopy(ASSISTANT_CONTENT_DEBUG_MESSAGE)
            finish_reason = ChatCompletionFinishReason.stop
        else:
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
            output_message = ChatCompletionAssistantMessage(content=message_content)
            finish_reason = ChatCompletionFinishReason.stop

        input_tokens = estimate_input_tokens(
            [message.model_dump() for message in messages],
            [function.model_dump() for function in functions] if functions else None,
            function_call,
        )
        output_tokens = estimate_response_tokens(output_message.model_dump())
        usage = ChatCompletionUsage(input_tokens=input_tokens, output_tokens=output_tokens)
        response = ChatCompletion(
            created_timestamp=get_current_timestamp_int(),
            finish_reason=finish_reason,
            message=output_message,
            usage=usage,
        )
        yield response
