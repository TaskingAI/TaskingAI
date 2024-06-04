from typing import Tuple, Dict

from app.models import ModelSchema
from provider_dependency.chat_completion import *

logger = logging.getLogger(__name__)


def _extract_system_message(messages: List[ChatCompletionMessage]) -> Tuple[Optional[str], List[ChatCompletionMessage]]:
    return None, messages


def _build_reka_message(message: ChatCompletionMessage):
    formatted_message = {"type": message.role.name, "text": []}
    if message.role == ChatCompletionRole.user:
        if isinstance(message.content, str):
            formatted_message["text"] = str(message.content)
        elif isinstance(message.content, List):
            check_valid_list_content(message.content)
            for content in message.content:
                if content.type == "text":
                    formatted_message["text"].append({"type": "text", "text": content.text})

        formatted_message["type"] = "human"

    if is_assistant_text_message(message):
        formatted_message["text"] = str(message.content)
        formatted_message["type"] = "model"

    return formatted_message


def _build_reka_header(credentials: ProviderCredentials):
    return {
        "x-api-key": f" {credentials.REKA_API_KEY}",
        "Content-Type": "application/json",
    }


def _build_reka_chat_completion_payload(
    messages: List[ChatCompletionMessage],
    stream: bool,
    provider_model_id: str,
    configs: ChatCompletionModelConfiguration,
    functions: Optional[List[ChatCompletionFunction]] = None,
):
    # Convert ChatCompletionMessages to the required format
    system_message, other_messages = _extract_system_message(messages)
    formatted_messages = [_build_reka_message(msg) for msg in other_messages]
    payload = {"conversation_history": formatted_messages, "model_name": provider_model_id, "stream": stream}

    config_dict = configs.model_dump()
    for key, value in config_dict.items():
        if value is not None:
            if key == "stop":
                if isinstance(value, list):
                    if all(isinstance(item, str) for item in value):
                        payload["stop_words"] = value
                    else:
                        payload["stop_words"] = [str(item) for item in value]
                else:
                    payload["stop_words"] = [str(value)]
            elif key == "top_p":
                payload["runtime_top_p"] = value
            elif key == "top_k":
                payload["runtime_top_k"] = value
            elif key == "max_tokens":
                payload["request_output_len"] = value
            elif key == "seed":
                payload["random_seed"] = value
            else:
                payload[key] = value
    return payload


class RekaChatCompletionModel(BaseChatCompletionModel):
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
        if stream and functions:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR, "Function calls for Claude are not supported in stream mode."
            )
        # todo accept user's api_url
        api_url = f"https://api.reka.ai/chat"
        headers = _build_reka_header(credentials)
        payload = _build_reka_chat_completion_payload(messages, stream, provider_model_id, configs, functions)
        return api_url, headers, payload

    # ------------------- handle non-stream chat completion response -------------------

    def extract_core_data(self, response_data: Dict, **kwargs) -> Optional[Dict]:
        if not response_data.get("text"):
            return None
        return response_data

    def extract_usage_data(self, response_data: Dict, **kwargs) -> Tuple[Optional[int], Optional[int]]:
        usage = response_data.get("metadata") if response_data else {}
        return usage.get("input_tokens", None), usage.get("generated_tokens", None)

    def extract_text_content(self, data: Dict, **kwargs) -> Optional[str]:
        message_data = data.get("text")
        if message_data:
            return message_data
        return None

    def extract_function_calls(self, data: Dict, **kwargs) -> Optional[List[ChatCompletionFunctionCall]]:
        return None

    def extract_finish_reason(self, data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        finish_reason = data.get("finish_reason", "unknown")
        return ChatCompletionFinishReason.__members__.get(finish_reason, ChatCompletionFinishReason.unknown)

    # ------------------- handle stream chat completion response -------------------

    def stream_check_error(self, sse_data: Dict, **kwargs):
        if sse_data.get("error"):
            raise_provider_api_error(sse_data["error"])

    def stream_extract_chunk_data(self, sse_data: Dict, **kwargs) -> Optional[Dict]:
        if not sse_data:
            return None
        return sse_data

    def stream_extract_usage_data(
        self, sse_data: Dict, input_tokens: int, output_tokens: int, **kwargs
    ) -> Tuple[int, int]:
        usage = sse_data.get("metadata") if sse_data else None
        if usage is not None:
            input_tokens = max(input_tokens or 0, usage.get("input_tokens", 0))
            output_tokens = max(output_tokens or 0, usage.get("generated_tokens", 0))
        return input_tokens, output_tokens

    def stream_extract_chunk(
        self, index: int, chunk_data: Dict, text_content: str, **kwargs
    ) -> Tuple[int, Optional[ChatCompletionChunk]]:
        content = chunk_data["text"] if chunk_data else None
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
            return ChatCompletionFinishReason.__members__.get(reason, ChatCompletionFinishReason.unknown)
        return None

    def stream_handle_function_calls(
        self, chunk_data: Dict, function_calls_content: ChatCompletionFunctionCallsContent, **kwargs
    ) -> Optional[ChatCompletionFunctionCallsContent]:
        return None
