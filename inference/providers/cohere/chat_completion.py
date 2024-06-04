from typing import Dict, Tuple

from app.models import ModelSchema
from provider_dependency.chat_completion import *

logger = logging.getLogger(__name__)

cohere_finish_reason_map = {
    "COMPLETE": ChatCompletionFinishReason.stop,
    "MAX_TOKENS": ChatCompletionFinishReason.length,
    "ERROR_LIMIT": ChatCompletionFinishReason.length,
    "ERROR_TOXIC": ChatCompletionFinishReason.error,
    "ERROR": ChatCompletionFinishReason.error,
    "USER_CANCEL": ChatCompletionFinishReason.unknown,
}


def _split_messages(messages: List[ChatCompletionMessage]) -> Tuple[str, List[Dict]]:
    # Validate input list to ensure it has elements.
    if not messages:
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "No messages provided")

    # Use list comprehension for a more concise and Pythonic way to build chat_history.
    chat_history = [_build_cohere_message(msg) for msg in messages[:-1]]

    # Directly access the last message, avoiding the need to pop from the list.
    latest_message = _build_cohere_message(messages[-1])
    message = latest_message["message"]

    return message, chat_history


def _build_cohere_message(message: ChatCompletionMessage):
    if message.role == ChatCompletionRole.system:
        return {"role": message.role.name, "message": message.content}

    if message.role == ChatCompletionRole.user:
        if isinstance(message.content, str):
            return {"role": message.role.name, "message": message.content}
        elif isinstance(message.content, List):
            text_message = ""
            for c in message.content:
                if c.type == "text":
                    text_message += c.text
            return {"role": message.role.name, "message": text_message}

    if is_assistant_text_message(message):
        return {"role": message.role.name, "message": message.content}


def _build_cohere_chat_completion_payload(
    messages: List[ChatCompletionMessage],
    stream: bool,
    provider_model_id: str,
    configs: ChatCompletionModelConfiguration,
):
    # Convert ChatCompletionMessages to the required format
    message, chat_history = _split_messages(messages)
    payload = {
        "chat_history": chat_history,
        "model": provider_model_id,
        "stream": stream,
        "message": message,
    }
    config_dict = configs.model_dump()
    for key, value in config_dict.items():
        if value is not None:
            if key == "top_p":
                payload["p"] = value
            elif key == "top_k":
                payload["k"] = value
            else:
                payload[key] = value

    return payload


class CohereChatCompletionModel(BaseChatCompletionModel):
    def __init__(self):
        super().__init__()

    # ------------------- prepare request data -------------------

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
        # todo accept user's api_url
        api_url = "https://api.cohere.ai/v1/chat"
        headers = {
            "Authorization": f"Bearer {credentials.COHERE_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = _build_cohere_chat_completion_payload(
            messages,
            stream,
            provider_model_id,
            configs,
        )
        return api_url, headers, payload

    # ------------------- handle non-stream chat completion response -------------------

    def extract_core_data(self, response_data: Dict, **kwargs) -> Optional[Dict]:
        return response_data

    def extract_usage_data(self, response_data: Dict, **kwargs) -> Tuple[Optional[int], Optional[int]]:
        meta = response_data.get("meta") if response_data else {}
        usage = meta.get("billed_units") if response_data else {}
        return usage.get("input_tokens", None), usage.get("output_tokens", None)

    def extract_text_content(self, data: Dict, **kwargs) -> Optional[str]:
        message_data = data.get("text")
        if message_data is None:
            return None
        return message_data

    def extract_function_calls(self, data: Dict, **kwargs) -> Optional[List[ChatCompletionFunctionCall]]:
        pass

    def extract_finish_reason(self, data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        finish_reason = data.get("finish_reason", "unknown")
        if finish_reason in cohere_finish_reason_map.keys():
            finish_reason = cohere_finish_reason_map.get(finish_reason)
        return ChatCompletionFinishReason.__members__.get(finish_reason, ChatCompletionFinishReason.unknown)

    # ------------------- handle stream chat completion response -------------------

    def stream_check_error(self, sse_data: Dict, **kwargs):
        if sse_data.get("error"):
            raise_provider_api_error(sse_data["error"])

    def stream_extract_chunk_data(self, sse_data: Dict, **kwargs) -> Optional[Dict]:
        return sse_data

    def stream_extract_usage_data(
        self, sse_data: Dict, input_tokens: int, output_tokens: int, **kwargs
    ) -> Tuple[int, int]:
        response = sse_data.get("response") if sse_data else {}
        meta = response.get("meta") if response else {}
        usage = meta.get("billed_units") if sse_data else None
        if usage is not None:
            input_tokens = max(input_tokens or 0, usage.get("input_tokens", 0))
            output_tokens = max(output_tokens or 0, usage.get("output_tokens", 0))
        return input_tokens, output_tokens

    def stream_extract_chunk(
        self, index: int, chunk_data: Dict, text_content: str, **kwargs
    ) -> Tuple[int, Optional[ChatCompletionChunk]]:
        content = chunk_data.get("text", {})
        if content:
            return index + 1, ChatCompletionChunk(
                created_timestamp=get_current_timestamp_int(),
                index=index,
                delta=content,
            )
        return index, None

    def stream_extract_finish_reason(self, chunk_data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        if chunk_data.get("finish_reason"):
            reason = chunk_data["finish_reason"]
            if reason in cohere_finish_reason_map.keys():
                reason = cohere_finish_reason_map.get(reason)
            return ChatCompletionFinishReason.__members__.get(reason, ChatCompletionFinishReason.unknown)
        return None

    def stream_handle_function_calls(
        self, chunk_data: Dict, function_calls_content: ChatCompletionFunctionCallsContent, **kwargs
    ) -> Optional[ChatCompletionFunctionCallsContent]:
        pass
