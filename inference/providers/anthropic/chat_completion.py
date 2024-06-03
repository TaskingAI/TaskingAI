from typing import Tuple, Dict
from provider_dependency.chat_completion import *

logger = logging.getLogger(__name__)


def _extract_system_message(messages: List[ChatCompletionMessage]) -> Tuple[Optional[str], List[ChatCompletionMessage]]:
    if messages and messages[0].role == ChatCompletionRole.system:
        return messages[0].content, messages[1:]
    return None, messages


def _build_anthropic_message(message: ChatCompletionMessage):
    formatted_message = {"role": message.role.name, "content": []}
    if message.role == ChatCompletionRole.user:
        if isinstance(message.content, str):
            formatted_message["content"].append({"type": "text", "text": str(message.content)})
        elif isinstance(message.content, List):
            check_valid_list_content(message.content)
            for content in message.content:
                if content.type == "text":
                    formatted_message["content"].append({"type": "text", "text": content.text})
                elif content.type == "image_url":
                    inline_data = {}
                    image_format, encoding_content = split_url(content.image_url.url)
                    inline_data["type"] = "image"
                    inline_data["source"] = {
                        "type": "base64",
                        "media_type": "image/" + image_format,
                        "data": encoding_content,
                    }
                    formatted_message["content"].append(inline_data)

    if is_assistant_text_message(message):
        formatted_message["content"].append({"type": "text", "text": str(message.content)})

    if message.role == ChatCompletionRole.function:
        message: ChatCompletionFunctionMessage
        formatted_message["role"] = "user"
        formatted_message["content"].append(
            {
                "type": "tool_result",
                "tool_use_id": message.id,
                "content": message.content,
            }
        )

    if is_assistant_function_calls_message(message):
        message: ChatCompletionAssistantMessage
        for f in message.function_calls:
            arguments = f.arguments
            formatted_message["content"].append(
                {
                    "id": f.id,
                    "type": "tool_use",
                    "name": f.name,
                    "input": arguments,
                }
            )

    return formatted_message


def _build_anthropic_header(credentials: ProviderCredentials):
    api_version = credentials.ANTHROPIC_API_VERSION
    if not api_version:
        api_version = "2023-06-01"
    return {
        "x-api-key": f" {credentials.ANTHROPIC_API_KEY}",
        "Content-Type": "application/json",
        "anthropic-version": f" {api_version}",
        "anthropic-beta": "tools-2024-04-04",
    }


def _build_anthropic_chat_completion_payload(
    messages: List[ChatCompletionMessage],
    stream: bool,
    provider_model_id: str,
    configs: ChatCompletionModelConfiguration,
    functions: Optional[List[ChatCompletionFunction]] = None,
):
    # Convert ChatCompletionMessages to the required format
    system_message, other_messages = _extract_system_message(messages)
    formatted_messages = [_build_anthropic_message(msg) for msg in other_messages]
    payload = {
        "messages": formatted_messages,
        "model": provider_model_id,
        "max_tokens": 4096,
        "stream": stream,
    }
    if system_message:
        payload["system"] = system_message

    if functions:
        tools = []
        for function in functions:
            tool = {
                "name": function.name,
                "description": function.description,
                "input_schema": function.parameters.model_dump(),
            }
            tools.append(tool)
        payload["tools"] = tools

    config_dict = configs.model_dump()
    for key, value in config_dict.items():
        if value is not None:
            if key == "stop":
                if isinstance(value, list):
                    if all(isinstance(item, str) for item in value):
                        payload["stop_sequences"] = value
                    else:
                        payload["stop_sequences"] = [str(item) for item in value]
                else:
                    payload["stop_sequences"] = [str(value)]
            else:
                payload[key] = value

    if configs.response_format:
        payload.pop("response_format", None)

        if configs.response_format == "json_object":
            payload["messages"][-1]["content"] = f"{payload['messages'][-1]['content']} Please respond in JSON format."
            if system_message:
                payload["system"] = f"{payload['system']} You are designed to output in JSON format."
            else:
                payload["system"] = "You are designed to output in JSON format."

    return payload


class AnthropicChatCompletionModel(BaseChatCompletionModel):
    def __init__(self):
        super().__init__()

    # ------------------- prepare request data -------------------

    def prepare_request(
        self,
        stream: bool,
        provider_model_id: str,
        messages: List[ChatCompletionMessage],
        credentials: ProviderCredentials,
        configs: ChatCompletionModelConfiguration,
        function_call: Optional[str] = None,
        functions: Optional[List[ChatCompletionFunction]] = None,
    ) -> Tuple[str, Dict, Dict]:
        # todo accept user's api_url
        api_url = f"https://api.anthropic.com/v1/messages"
        headers = _build_anthropic_header(credentials)
        payload = _build_anthropic_chat_completion_payload(messages, stream, provider_model_id, configs, functions)
        return api_url, headers, payload

    # ------------------- handle non-stream chat completion response -------------------

    def extract_core_data(self, response_data: Dict, **kwargs) -> Optional[Dict]:
        if not response_data.get("content"):
            return None
        return response_data

    def extract_text_content(self, data: Dict, **kwargs) -> Optional[str]:
        message_data = data.get("content")
        if message_data and message_data[0].get("text"):
            return message_data[0].get("text")
        return None

    def extract_function_calls(self, data: Dict, **kwargs) -> Optional[List[ChatCompletionFunctionCall]]:
        if data and isinstance(data["content"], list):
            function_calls = []
            for message in data["content"]:
                if message.get("type") == "tool_use":
                    func_call = build_function_call(
                        name=message["name"],
                        arguments_dict=message["input"],
                    )
                    function_calls.append(func_call)
            return function_calls if function_calls else None
        return None

    def extract_finish_reason(self, data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        finish_reason = data.get("stop_reason", "unknown")
        if finish_reason == "tool_use":
            finish_reason = ChatCompletionFinishReason.function_calls
        if finish_reason == "max_tokens":
            finish_reason = ChatCompletionFinishReason.length
        if finish_reason in ["end_turn", "stop_sequence"]:
            finish_reason = ChatCompletionFinishReason.stop
        return ChatCompletionFinishReason.__members__.get(finish_reason, ChatCompletionFinishReason.unknown)

    # ------------------- handle stream chat completion response -------------------

    def stream_check_error(self, sse_data: Dict, **kwargs):
        if sse_data.get("error"):
            raise_provider_api_error(sse_data["error"])

    def stream_extract_chunk_data(self, sse_data: Dict, **kwargs) -> Optional[Dict]:
        if sse_data.get("delta") is None:
            return None
        return sse_data

    def stream_extract_chunk(
        self, index: int, chunk_data: Dict, text_content: str, **kwargs
    ) -> Tuple[int, Optional[ChatCompletionChunk]]:
        if chunk_data and chunk_data.get("delta") and chunk_data.get("delta").get("type") == "text_delta":
            return index + 1, ChatCompletionChunk(
                created_timestamp=get_current_timestamp_int(),
                index=index,
                delta=chunk_data["delta"]["text"],
            )
        return index, None

    def stream_extract_finish_reason(self, chunk_data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        if chunk_data.get("delta"):
            finish_reason = chunk_data.get("delta", {}).get("stop_reason")
            if finish_reason == "tool_use":
                finish_reason = ChatCompletionFinishReason.function_calls
            if finish_reason == "max_tokens":
                finish_reason = ChatCompletionFinishReason.length
            if finish_reason in ["end_turn", "stop_sequence"]:
                finish_reason = ChatCompletionFinishReason.stop
            return ChatCompletionFinishReason.__members__.get(finish_reason, ChatCompletionFinishReason.unknown)
        return None

    def stream_handle_function_calls(
        self, chunk_data: Dict, function_calls_content: ChatCompletionFunctionCallsContent, **kwargs
    ) -> Optional[ChatCompletionFunctionCallsContent]:
        pass
