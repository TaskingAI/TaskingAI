from app.models import ModelSchema
from provider_dependency.chat_completion import *
from .utils import build_zhipu_header
from typing import Tuple, Dict

logger = logging.getLogger(__name__)


def _build_zhipu_message(message: ChatCompletionMessage):
    if message.role == ChatCompletionRole.system:
        return {"role": message.role.name, "content": message.content}

    if message.role == ChatCompletionRole.user:
        if isinstance(message.content, str):
            return {"role": message.role.name, "content": message.content}
        elif isinstance(message.content, List):
            check_valid_list_content(message.content)
            content = [c.model_dump() for c in message.content]
            return {
                "role": message.role.name,
                "content": content,
            }

    if message.role == ChatCompletionRole.function:
        message: ChatCompletionFunctionMessage
        return {"role": "tool", "content": message.content, "tool_call_id": message.id}

    if is_assistant_text_message(message):
        return {"role": message.role.name, "content": message.content}

    if is_assistant_function_calls_message(message):
        message: ChatCompletionAssistantMessage
        function_calls = []

        for f in message.function_calls:
            arguments = f.arguments
            if isinstance(arguments, dict):
                arguments = json.dumps(arguments)
            function_calls.append(
                {
                    "id": f.id,
                    "type": "function",
                    "function": {"name": f.name, "arguments": arguments},
                }
            )

        return {
            "role": ChatCompletionRole.assistant.name,
            "tool_calls": function_calls,
            "content": None,
        }


def _build_zhipu_chat_completion_payload(
    messages: List[ChatCompletionMessage],
    stream: bool,
    provider_model_id: str,
    configs: ChatCompletionModelConfiguration,
    function_call: Optional[str],
    functions: Optional[List[ChatCompletionFunction]],
):
    # Convert ChatCompletionMessages to the required format
    formatted_messages = [_build_zhipu_message(msg) for msg in messages]
    logger.debug("formatted_messages: %s", formatted_messages)
    payload = {
        "messages": formatted_messages,
        "model": provider_model_id,
        "stream": stream,
    }
    config_dict = configs.model_dump()
    value_adjustments = {1: 0.99, 0: 0.01}
    for key, value in config_dict.items():
        if value is not None:
            if key == "temperature" or key == "top_p":
                value = value_adjustments.get(value, value)
            payload[key] = value
    if function_call:
        if function_call in ["none", "auto"]:
            payload["tool_choice"] = function_call
        else:
            payload["tool_choice"] = {"name": function_call}
    if functions:
        payload["tools"] = [{"type": "function", "function": f.model_dump()} for f in functions]
    return payload


def _parse_function_call_arguments(func_call_id: str, function_name: str, function_call_arguments_str: str):
    logger.debug(f"_parse_function_call_arguments = {function_name}")
    try:
        argument_dict = json.loads(function_call_arguments_str)
        function_call = ChatCompletionFunctionCall(id=func_call_id, name=function_name, arguments=argument_dict)
        return function_call
    except json.decoder.JSONDecodeError:
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR)


class ZhipuChatCompletionModel(BaseChatCompletionModel):
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
        api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = build_zhipu_header(credentials)
        payload = _build_zhipu_chat_completion_payload(
            messages, stream, provider_model_id, configs, function_call, functions
        )
        return api_url, headers, payload

    # ------------------- handle non-stream chat completion response -------------------

    def extract_core_data(self, response_data: Dict, **kwargs) -> Optional[Dict]:
        if not response_data.get("choices"):
            return None
        return response_data["choices"][0]

    def extract_usage_data(self, response_data: Dict, **kwargs) -> Tuple[Optional[int], Optional[int]]:
        usage = response_data.get("usage") if response_data else {}
        return usage.get("prompt_tokens", None), usage.get("completion_tokens", None)

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
        if finish_reason == "sensitive":
            raise_provider_api_error("Zhipu content filter triggered, content was omitted")
        if finish_reason == "network_error":
            finish_reason = ChatCompletionFinishReason.error
        return ChatCompletionFinishReason.__members__.get(finish_reason, ChatCompletionFinishReason.unknown)

    # ------------------- handle stream chat completion response -------------------
    def stream_check_error(self, sse_data: Dict, **kwargs):
        if sse_data.get("error"):
            raise_provider_api_error(sse_data["error"])

    def stream_extract_chunk_data(self, sse_data: Dict, **kwargs) -> Optional[Dict]:
        if not sse_data.get("choices"):
            return None
        return sse_data["choices"][0]

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
        content = chunk_data.get("delta", {}).get("content") if chunk_data else None
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
            if reason == "tool_calls":
                reason = ChatCompletionFinishReason.function_calls
            if reason == "sensitive":
                raise_provider_api_error("Zhipu content filter triggered, content was omitted")
            if reason == "network_error":
                reason = ChatCompletionFinishReason.error
            return ChatCompletionFinishReason.__members__.get(reason, ChatCompletionFinishReason.unknown)
        return None

    def stream_handle_function_calls(
        self, chunk_data: Dict, function_calls_content: ChatCompletionFunctionCallsContent, **kwargs
    ) -> Optional[ChatCompletionFunctionCallsContent]:
        delta = chunk_data.get("delta", {})
        if delta and delta.get("tool_calls"):
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
