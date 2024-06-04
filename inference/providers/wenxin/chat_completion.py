import json
import logging
from typing import Dict, List, Optional, Tuple

from app.models import ModelSchema
from provider_dependency.chat_completion import (
    BaseChatCompletionModel,
    ChatCompletionChunk,
    ChatCompletionFinishReason,
    ChatCompletionFunction,
    ChatCompletionFunctionCall,
    ChatCompletionFunctionCallsContent,
    ChatCompletionMessage,
    ChatCompletionModelConfiguration,
    ChatCompletionRole,
    ProviderCredentials,
    build_function_call,
    get_current_timestamp_int,
    is_assistant_function_calls_message,
    raise_provider_api_error,
)

from .utils import generate_access_token

logger = logging.getLogger(__name__)


def _build_wenxin_chat_completion_payload(
    messages: List[ChatCompletionMessage],
    stream: bool,
    configs: ChatCompletionModelConfiguration,
    function_call: Optional[str],
    functions: Optional[List[ChatCompletionFunction]],
):
    # Helper function to handle message formatting
    def format_message(msg):
        base_message = {"role": msg.role.name, "content": msg.content}
        if msg.role == ChatCompletionRole.function:
            base_message.update({"name": functions_map.get(msg.id, "")})
        elif is_assistant_function_calls_message(msg):
            f = msg.function_calls[0]
            arguments = json.dumps(f.arguments) if isinstance(f.arguments, dict) else f.arguments
            base_message.update(
                {
                    "function_call": {"name": f.name, "arguments": arguments},
                    "content": None,
                }
            )
        return base_message

    # Convert ChatCompletionMessages to the required format
    functions_map = {
        msg.function_calls[0].id: msg.function_calls[0].name
        for msg in messages
        if is_assistant_function_calls_message(msg)
    }
    formatted_messages = [format_message(msg) for msg in messages]

    # Construct payload
    payload = {"messages": formatted_messages, "stream": stream}
    for k, v in configs.model_dump().items():
        if v is not None:
            if k == "max_tokens":
                payload["max_output_tokens"] = v
            else:
                payload[k] = v

    if function_call:
        if function_call in ["none", "auto"]:
            payload["tool_choice"] = function_call
        else:
            payload["tool_choice"] = {"name": function_call}

    if functions:
        payload["functions"] = [f.model_dump() for f in functions]

    return payload


class WenxinChatCompletionModel(BaseChatCompletionModel):
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
        endpoint = {
            "ernie-bot": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions",
            "ernie-bot-4": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro",
            "ernie-bot-8k": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_bot_8k",
            "ernie-bot-turbo": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant",
        }
        # todo accept user's api_url
        access_token = generate_access_token(credentials).access_token
        api_url = f"{endpoint[provider_model_id]}?access_token={access_token}"
        headers = {"Content-Type": "application/json"}
        payload = _build_wenxin_chat_completion_payload(messages, stream, configs, function_call, functions)
        return api_url, headers, payload

    # ------------------- handle non-stream chat completion response -------------------

    def extract_core_data(self, response_data: Dict, **kwargs) -> Optional[Dict]:
        if response_data.get("error_code"):
            raise_provider_api_error(str(response_data))
        return response_data

    def extract_usage_data(self, response_data: Dict, **kwargs) -> Tuple[Optional[int], Optional[int]]:
        usage = response_data.get("usage") if response_data else {}
        return usage.get("prompt_tokens", None), usage.get("completion_tokens", None)

    def extract_text_content(self, data: Dict, **kwargs) -> Optional[str]:
        message_data = data.get("result")
        return message_data

    def extract_function_calls(self, data: Dict, **kwargs) -> Optional[List[ChatCompletionFunctionCall]]:
        if data.get("function_call"):
            function_calls = []
            function_call = data.get("function_call")
            call = build_function_call(
                name=function_call["name"],
                arguments_str=function_call["arguments"],
            )
            function_calls.append(call)
            return function_calls
        return None

    def extract_finish_reason(self, data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        finish_reason = data.get("finish_reason", "unknown")
        if finish_reason == "function_call":
            finish_reason = ChatCompletionFinishReason.function_calls
        if finish_reason == "normal":
            finish_reason = "stop"
        if finish_reason == "content_filter":
            raise_provider_api_error("Wenxin content filter triggered, content was omitted")
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
        usage = sse_data.get("usage") if sse_data else None
        if usage is not None:
            input_tokens = max(input_tokens or 0, usage.get("prompt_tokens", 0))
            output_tokens = max(output_tokens or 0, usage.get("completion_tokens", 0))
        return input_tokens, output_tokens

    def stream_extract_chunk(
        self, index: int, chunk_data: Dict, text_content: str, **kwargs
    ) -> Tuple[int, Optional[ChatCompletionChunk]]:
        delta = chunk_data["result"]
        if delta:
            return index + 1, ChatCompletionChunk(
                created_timestamp=get_current_timestamp_int(),
                index=index,
                delta=delta,
            )
        return index, None

    def stream_extract_finish_reason(self, chunk_data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        if chunk_data.get("finish_reason"):
            finish_reason = chunk_data["finish_reason"]
            if finish_reason == "function_call":
                finish_reason = ChatCompletionFinishReason.function_calls
            if finish_reason == "normal":
                finish_reason = "stop"
            if finish_reason == "content_filter":
                raise_provider_api_error("Wenxin content filter triggered, content was omitted")
            return ChatCompletionFinishReason.__members__.get(finish_reason, ChatCompletionFinishReason.unknown)
        return None

    def stream_handle_function_calls(
        self, chunk_data: Dict, function_calls_content: ChatCompletionFunctionCallsContent, **kwargs
    ) -> Optional[ChatCompletionFunctionCallsContent]:
        if chunk_data.get("function_call"):
            tool_call = chunk_data["function_call"]
            function_calls_content.arguments_strs.append(tool_call["arguments"])
            function_calls_content.names.append(tool_call["name"])
            return function_calls_content

        return None
