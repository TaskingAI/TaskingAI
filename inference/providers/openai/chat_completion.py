from typing import Tuple, Dict

from app.models import ModelSchema
from app.utils.utils import image_url_is_on_localhost, fetch_image_format, get_image_base64_string
from provider_dependency.chat_completion import *
from .utils import *

logger = logging.getLogger(__name__)


async def construct_image_data(image_url: str) -> dict:
    if image_url_is_on_localhost(image_url):
        image_format = await fetch_image_format(image_url)
        base64_string = await get_image_base64_string(image_url)

        return {"type": "image_url", "image_url": {"url": f"data:image/{image_format};base64,{base64_string}"}}

    # Normal image url
    if "http" in image_url:
        return {"type": "image_url", "image_url": {"url": image_url}}

    raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid image url.")


async def split_markdown_to_objects_preserve_order(markdown_content):
    import re

    # Define regex pattern for extracting text and images
    pattern = re.compile(r"(!\[.*?\]\(.*?\))|([^!]+)", re.MULTILINE)

    # Find all matches
    matches = pattern.findall(markdown_content)

    # Split the content into a list of objects
    result = []

    for match in matches:
        if match[0]:  # This is an image
            image_url = re.findall(r"!\[.*?\]\((.*?)\)", match[0])[0]
            result.append(await construct_image_data(image_url))
        elif match[1].strip():  # This is text
            result.append({"type": "text", "text": match[1].strip()})

    return result


async def _build_openai_message(message: ChatCompletionMessage, vision_support: bool = False):
    if message.role == ChatCompletionRole.system:
        return {"role": message.role.name, "content": message.content}

    if message.role == ChatCompletionRole.user:
        if isinstance(message.content, str):
            return {
                "role": message.role.name,
                "content": await split_markdown_to_objects_preserve_order(message.content)
                if vision_support
                else message.content,
            }
        elif isinstance(message.content, List):
            return {
                "role": message.role.name,
                "content": [c.model_dump() for c in message.content],
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


async def _build_openai_chat_completion_payload(
    messages: List[ChatCompletionMessage],
    stream: bool,
    provider_model_id: str,
    configs: ChatCompletionModelConfiguration,
    function_call: Optional[str],
    functions: Optional[List[ChatCompletionFunction]],
    vision_support: bool = False,
):
    # Convert ChatCompletionMessages to the required format
    formatted_messages = []
    for message in messages[:-1]:
        formatted_messages.append(await _build_openai_message(message, vision_support=False))
    formatted_messages.append(await _build_openai_message(messages[-1], vision_support=vision_support))
    logger.debug("formatted_messages: %s", formatted_messages)
    payload = {
        "messages": formatted_messages,
        "model": provider_model_id,
        "stream": stream,
    }
    if stream:
        payload["stream_options"] = {"include_usage": True}

    config_dict = configs.model_dump()
    for key, value in config_dict.items():
        if value is not None:
            payload[key] = value

    if configs.response_format:
        payload["response_format"] = {"type": configs.response_format}

        if configs.response_format == "json_object":

            if payload["messages"][0]["role"] == "system":
                payload["messages"][0][
                    "content"
                ] = f"{payload['messages'][0]['content']} You are designed to output JSON."
            else:
                payload["messages"].insert(0, {"role": "system", "content": "You are designed to output JSON."})

    if "max_tokens" not in payload and "vision" in provider_model_id:
        # OpenAI currently set a low max_tokens default, so we need to override it
        payload["max_tokens"] = 4096

    if function_call:
        if function_call in ["none", "auto"]:
            payload["tool_choice"] = function_call
        else:
            payload["tool_choice"] = {"name": function_call}
    if functions:
        payload["tools"] = [{"type": "function", "function": f.model_dump()} for f in functions]
    logger.debug(f"_build_openai_chat_completion_payload: {payload}")
    return payload


class OpenaiChatCompletionModel(BaseChatCompletionModel):
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
        api_url = "https://api.openai.com/v1/chat/completions"
        headers = build_openai_header(credentials)
        payload = await _build_openai_chat_completion_payload(
            messages, stream, provider_model_id, configs, function_call, functions, model_schema.allow_vision_input()
        )
        return api_url, headers, payload

    # ------------------- handle non-stream chat completion response -------------------

    def extract_core_data(self, response_data: Dict, **kwargs) -> Optional[Dict]:
        if not response_data.get("choices"):
            return None
        return response_data["choices"][0]

    def extract_usage_data(self, response_data: Dict, **kwargs) -> Tuple[Optional[int], Optional[int]]:
        usage = response_data.get("usage") if response_data else None
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
        if finish_reason == "content_filter":
            raise_provider_api_error("Openai content filter triggered, content was omitted")
        return ChatCompletionFinishReason.__members__.get(finish_reason, ChatCompletionFinishReason.unknown)

    # ------------------- handle stream chat completion response -------------------

    def stream_check_error(self, sse_data: Dict, **kwargs):
        if sse_data.get("error"):
            raise_provider_api_error(sse_data["error"])

    def stream_extract_chunk_data(self, sse_data: Dict, **kwargs) -> Optional[Dict]:
        if not sse_data.get("choices"):
            return None
        return sse_data["choices"][0]

    def stream_extract_usage_data(self, sse_data: Dict, input_tokens, output_tokens, **kwargs) -> Tuple[int, int]:
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
            if reason == "content_filter":
                raise_provider_api_error("Openai content filter triggered, content was omitted")
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
