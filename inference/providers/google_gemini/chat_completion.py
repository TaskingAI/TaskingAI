import json

from app.models import ModelSchema
from app.utils.utils import fetch_image_format, get_image_base64_string
from provider_dependency.chat_completion import *
from typing import Tuple, Dict

logger = logging.getLogger(__name__)


google_gemini_finish_reason_map = {
    "STOP": ChatCompletionFinishReason.stop,
    "MAX_TOKENS": ChatCompletionFinishReason.length,
    "RECITATION": ChatCompletionFinishReason.recitation,
    "SAFETY": ChatCompletionFinishReason.error,
    "FINISH_REASON_UNSPECIFIED": ChatCompletionFinishReason.unknown,
    "OTHER": ChatCompletionFinishReason.unknown,
}


def _build_google_gemini_header(credentials: ProviderCredentials):
    return {
        "x-goog-api-key": f" {credentials.GOOGLE_GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }


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
            image_format = await fetch_image_format(image_url)
            base64_string = await get_image_base64_string(image_url)
            result.append({"inlineData": {"mimeType": f"image/{image_format}", "data": base64_string}})
        elif match[1].strip():  # This is text
            result.append({"text": match[1].strip()})

    return result


async def _build_google_gemini_chat_completion_payload(
    messages: List[ChatCompletionMessage],
    configs: ChatCompletionModelConfiguration,
    function_call: Optional[str],
    functions: Optional[List[ChatCompletionFunction]],
    vision_support: bool = False,
):
    # Convert ChatCompletionMessages to the required format
    if len(messages) > 1 and messages[0].role == "system":
        # Append system message content to the next message.
        messages[1].content += messages[0].content
        # Remove the system message from the list.
        del messages[0]

    async def format_message(msg: ChatCompletionMessage, should_send_image_if_possible=False):
        if msg.role == ChatCompletionRole.user:
            if isinstance(msg.content, str):
                if vision_support and should_send_image_if_possible:
                    return {"role": msg.role.name, "parts": await split_markdown_to_objects_preserve_order(msg.content)}
                else:
                    return {"role": msg.role.name, "parts": [{"text": msg.content}]}
            elif isinstance(msg.content, List):
                check_valid_list_content(msg.content)
                formatted_msg = {"role": "user", "parts": []}
                for content in msg.content:
                    if content.type == "text":
                        formatted_msg["parts"].append({"text": content.text})
                    elif content.type == "image_url":
                        inline_data = {}
                        image_format, encoding_content = split_url(content.image_url.url)
                        inline_data["mimeType"] = "image/" + image_format
                        inline_data["data"] = encoding_content
                        formatted_msg["parts"].append({"inline_data": inline_data})
                return formatted_msg

        if msg.role == ChatCompletionRole.function:
            content = {}
            if isinstance(msg.content, str):
                content.update({"result": msg.content})
            elif isinstance(msg.content, dict):
                content.update(msg.content)
            return {
                "role": "function",
                "parts": [
                    {
                        "functionResponse": {
                            "name": functions_map.get(msg.id, ""),
                            "response": {"name": functions_map.get(msg.id, ""), "content": content},
                        }
                    }
                ],
            }

        if is_assistant_text_message(msg):
            return {"role": "model", "parts": [{"text": msg.content}]}

        if is_assistant_function_calls_message(msg):
            msg: ChatCompletionAssistantMessage
            function_calls = []

            for f in msg.function_calls:
                arguments = f.arguments
                function_calls.append(
                    {
                        "functionCall": {"name": f.name, "args": arguments},
                    }
                )

            return {
                "role": "model",
                "parts": function_calls,
            }

    # Convert ChatCompletionMessages to the required format
    functions_map = {
        msg.function_calls[0].id: msg.function_calls[0].name
        for msg in messages
        if is_assistant_function_calls_message(msg)
    }
    formatted_messages = []
    for message in messages[:-1]:
        formatted_messages.append(await format_message(message, should_send_image_if_possible=False))
    formatted_messages.append(await format_message(messages[-1], should_send_image_if_possible=True))
    generation_config = {}
    config_dict = configs.model_dump()
    for key, value in config_dict.items():
        if value is not None:
            if key == "max_tokens":
                generation_config["maxOutputTokens"] = value
            elif key == "top_p":
                generation_config["topP"] = value
            elif key == "top_k":
                generation_config["topK"] = value
            else:
                generation_config[key] = value

    if configs.response_format:
        generation_config.pop("response_format", None)
        if configs.response_format == "json_object":
            generation_config["response_mime_type"] = "application/json"

    payload = {"contents": formatted_messages, "generationConfig": generation_config}
    if functions:
        payload["tools"] = [{"functionDeclarations": [f.model_dump() for f in functions]}]
    return payload


class GoogleGeminiChatCompletionModel(BaseChatCompletionModel):
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
        if credentials.GOOGLE_GEMINI_API_VERSION == "v1" and functions:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR,
                "Function calls for Google Gemini are only supported in 'v1beta' API version.",
            )
        if (not credentials.GOOGLE_GEMINI_API_VERSION) and (functions or provider_model_id == "gemini-1.5-pro-latest"):
            api_version = "v1beta"
        else:
            api_version = credentials.GOOGLE_GEMINI_API_VERSION if credentials.GOOGLE_GEMINI_API_VERSION else "v1"

        action = "streamGenerateContent?alt=sse" if stream else "generateContent"
        api_url = f"https://generativelanguage.googleapis.com/{api_version}/models/{provider_model_id}:{action}"

        payload = await _build_google_gemini_chat_completion_payload(
            messages, configs, function_call, functions, model_schema.allow_vision_input()
        )
        headers = _build_google_gemini_header(credentials)
        return api_url, headers, payload

    # ------------------- handle non-stream chat completion response -------------------

    def extract_core_data(self, response_data: Dict, **kwargs) -> Optional[Dict]:
        if response_data.get("candidates") is None:
            raise_provider_api_error(json.dumps(response_data))
        return response_data["candidates"][0]

    def extract_usage_data(self, response_data: Dict, **kwargs) -> Tuple[Optional[int], Optional[int]]:
        usage_metadata = response_data.get("usageMetadata") if response_data else {}
        return usage_metadata.get("promptTokenCount", None), usage_metadata.get("candidatesTokenCount", None)

    def extract_text_content(self, data: Dict, **kwargs) -> Optional[str]:
        # Directly access the nested 'text' if all keys exist, else return None
        return data.get("content", {}).get("parts", [{}])[0].get("text") if data else None

    def extract_function_calls(self, data: Dict, **kwargs) -> Optional[List[ChatCompletionFunctionCall]]:
        parts = data.get("content", {}).get("parts", [])
        if not parts:
            return None

        first_part = parts[0]
        function_call_data = first_part.get("functionCall")
        # Check if function_call_data is not None before proceeding
        if function_call_data:
            return [build_function_call(name=function_call_data["name"], arguments_dict=function_call_data["args"])]

        return None

    def extract_finish_reason(self, data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        finish_reason = data.get("finishReason", "unknown")
        if finish_reason in google_gemini_finish_reason_map.keys():
            finish_reason = google_gemini_finish_reason_map.get(finish_reason)
        return ChatCompletionFinishReason.__members__.get(finish_reason, ChatCompletionFinishReason.unknown)

    # ------------------- handle stream chat completion response -------------------

    def stream_check_error(self, sse_data: Dict, **kwargs):
        if sse_data.get("error"):
            raise_provider_api_error(sse_data["error"])

    def stream_extract_chunk_data(self, sse_data: Dict, **kwargs) -> Optional[Dict]:
        if sse_data.get("candidates") is None:
            return None
        return sse_data["candidates"][0]

    def stream_extract_usage_data(
        self, sse_data: Dict, input_tokens: int, output_tokens: int, **kwargs
    ) -> Tuple[int, int]:
        usage_metadata = sse_data.get("usageMetadata") if sse_data else None
        if usage_metadata is not None:
            input_tokens = max(input_tokens or 0, usage_metadata.get("promptTokenCount", 0))
            output_tokens = max(output_tokens or 0, usage_metadata.get("candidatesTokenCount", 0))
        return input_tokens, output_tokens

    def stream_extract_chunk(
        self, index: int, chunk_data: Dict, text_content: str, **kwargs
    ) -> Tuple[int, Optional[ChatCompletionChunk]]:
        delta_text = chunk_data.get("content", {}).get("parts", [{}])[0].get("text")
        if delta_text:
            return index + 1, ChatCompletionChunk(
                created_timestamp=get_current_timestamp_int(),
                index=index,
                delta=delta_text,
            )
        return index, None

    def stream_extract_finish_reason(self, chunk_data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        if chunk_data.get("finishReason"):
            reason = chunk_data["finishReason"]
            if reason in google_gemini_finish_reason_map.keys():
                reason = google_gemini_finish_reason_map.get(reason)
            return ChatCompletionFinishReason.__members__.get(reason, ChatCompletionFinishReason.unknown)
        return None

    def stream_handle_function_calls(
        self, chunk_data: Dict, function_calls_content: ChatCompletionFunctionCallsContent, **kwargs
    ) -> Optional[ChatCompletionFunctionCallsContent]:
        function_call_content = chunk_data.get("content", {}).get("parts", [{}])[0]
        tool_call = function_call_content.get("functionCall")
        if tool_call:
            toll_call_index = 0

            if toll_call_index == function_calls_content.index:
                # append to the current function call argument string
                function_calls_content.arguments_dicts[function_calls_content.index] += tool_call["args"]

            elif toll_call_index > function_calls_content.index:
                # trigger another function call
                function_calls_content.arguments_dicts.append(tool_call["args"])
                function_calls_content.names.append(tool_call["name"])
                function_calls_content.index = toll_call_index
            return function_calls_content

        return None
