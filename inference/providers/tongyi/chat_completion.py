from typing import Tuple, Dict

from app.models import ModelSchema
from provider_dependency.chat_completion import *
from .utils import *

logger = logging.getLogger(__name__)


def _build_tongyi_message(message: ChatCompletionMessage):
    if message.role in [
        ChatCompletionRole.user,
        ChatCompletionRole.system,
    ] or is_assistant_text_message(message):
        return {"role": message.role.name, "content": message.content}


def _build_tongyi_chat_completion_payload(
    messages: List[ChatCompletionMessage],
    provider_model_id: str,
    configs: ChatCompletionModelConfiguration,
):
    # Convert ChatCompletionMessages to the required format
    formatted_messages = [_build_tongyi_message(msg) for msg in messages]
    logger.debug("formatted_messages: %s", formatted_messages)
    payload = {
        "input": {
            "messages": formatted_messages,
        },
        "model": provider_model_id,
        "parameters": {
            "result_format": "message",
        },
    }
    config_dict = configs.model_dump()
    for key, value in config_dict.items():
        if value is not None:
            payload["parameters"][key] = value
    return payload


class TongyiChatCompletionModel(BaseChatCompletionModel):
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
        api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        if not stream:
            headers = build_tongyi_header(credentials)
        else:
            headers = build_tongyi_header_stream(credentials)
        payload = _build_tongyi_chat_completion_payload(messages, provider_model_id, configs)
        return api_url, headers, payload

    # ------------------- handle non-stream chat completion response -------------------

    def extract_core_data(self, response_data: Dict, **kwargs) -> Optional[Dict]:
        if not response_data.get("output") or not response_data["output"].get("choices"):
            return None
        return response_data["output"]["choices"][0]

    def extract_usage_data(self, response_data: Dict, **kwargs) -> Tuple[Optional[int], Optional[int]]:
        usage = response_data.get("usage") if response_data else {}
        return usage.get("input_tokens", None), usage.get("output_tokens", None)

    def extract_text_content(self, data: Dict, **kwargs) -> Optional[str]:
        message_data = data.get("message") if data else None
        if message_data and message_data.get("content"):
            return message_data.get("content")
        return None

    def extract_function_calls(self, data: Dict, **kwargs) -> Optional[List[ChatCompletionFunctionCall]]:
        message_data = data.get("message") if data else None
        if message_data.get("tool_calls"):
            function_calls = []
            tool_calls = message_data.get("tool_calls")
            for call in tool_calls:
                func_call = build_function_call(
                    name=call["function"]["name"],
                    arguments_str=call["function"]["arguments"],
                )
                function_calls.append(func_call)
            return function_calls

        return None

    def extract_finish_reason(self, data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        finish_reason = data.get("finish_reason", "unknown")
        if finish_reason == "tool_calls":
            finish_reason = ChatCompletionFinishReason.function_calls
        if finish_reason == "content_filter":
            raise_provider_api_error("Tongyi content filter triggered, content was omitted")
        return ChatCompletionFinishReason.__members__.get(finish_reason, ChatCompletionFinishReason.unknown)

    # ------------------- handle stream chat completion response -------------------

    def stream_check_error(self, sse_data: Dict, **kwargs):
        if sse_data.get("error"):
            raise_provider_api_error(sse_data["error"])

    def stream_extract_chunk_data(self, sse_data: Dict, **kwargs) -> Optional[Dict]:
        if not sse_data.get("output") or not sse_data["output"].get("choices"):
            return None
        return sse_data["output"]["choices"][0]

    def stream_extract_usage_data(
        self, sse_data: Dict, input_tokens: int, output_tokens: int, **kwargs
    ) -> Tuple[int, int]:
        usage = sse_data.get("usage") if sse_data else None
        if usage is not None:
            input_tokens = max(input_tokens or 0, usage.get("input_tokens", 0))
            output_tokens = max(output_tokens or 0, usage.get("output_tokens", 0))
        return input_tokens, output_tokens

    def stream_extract_chunk(
        self, index: int, chunk_data: Dict, text_content: str, **kwargs
    ) -> Tuple[int, Optional[ChatCompletionChunk]]:
        delta = chunk_data["message"]
        if delta.get("content"):
            # remove the prefix of content
            new_content = delta["content"].replace(text_content, "", 1)

            return index + 1, ChatCompletionChunk(
                created_timestamp=get_current_timestamp_int(),
                index=index,
                delta=new_content,
            )
        return index, None

    def stream_extract_finish_reason(self, chunk_data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        if chunk_data.get("finish_reason") and chunk_data["finish_reason"] != "null":
            reason = chunk_data["finish_reason"]
            if reason == "tool_calls":
                reason = ChatCompletionFinishReason.function_calls
            if reason == "content_filter":
                raise_provider_api_error("Tongyi content filter triggered, content was omitted")
            return ChatCompletionFinishReason.__members__.get(reason, ChatCompletionFinishReason.unknown)
        return None

    def stream_handle_function_calls(
        self, chunk_data: Dict, function_calls_content: ChatCompletionFunctionCallsContent, **kwargs
    ) -> Optional[ChatCompletionFunctionCallsContent]:
        delta = chunk_data["message"]
        if delta.get("tool_calls"):
            tool_call = delta["tool_calls"][0]
            toll_call_index = tool_call["index"]
            tool_call_function = tool_call["function"]

            if toll_call_index == function_calls_content.index:
                # append to the current function call argument string
                function_calls_content.arguments_strs[function_calls_content.index] += tool_call_function["arguments"]

            elif toll_call_index > function_calls_content.index:
                # trigger another function call
                function_calls_content.arguments_strs.append(tool_call_function["arguments"] or "")
                function_calls_content.names.append(tool_call_function["name"])
                function_calls_content.index = toll_call_index
            return function_calls_content

        return None
