from app.models import ModelSchema
from provider_dependency.chat_completion import *
from typing import List, Optional, Dict, Tuple

logger = logging.getLogger(__name__)


def _build_hugging_face_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.HUGGING_FACE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _build_hugging_face_text_generation_message(messages: List[ChatCompletionMessage]):
    # Generate "Human" and "Assistant" dialogue parts

    prompt_parts = []
    for msg in messages:
        if msg.role == ChatCompletionRole.system:
            prompt_parts.append(f"Requirement: {msg.content}\n")
        elif msg.role == ChatCompletionRole.user:
            prompt_parts.append(f"Question: {msg.content} Let's think step by step. \n")
        elif msg.role == ChatCompletionRole.assistant:
            prompt_parts.append(f"Answer: {msg.content}\n")
    prompt = "".join(prompt_parts) + "Answer: "

    return prompt


def _build_hugging_face_text_generation_payload(
    messages: List[ChatCompletionMessage],
    stream: bool,
    provider_model_id: str,
    configs: ChatCompletionModelConfiguration,
):
    # Convert ChatCompletionMessages to the required format
    inputs = _build_hugging_face_text_generation_message(messages)
    logger.debug("inputs: %s", inputs)
    logger.debug("configs.max_tokens: %s", configs.max_tokens)
    payload = {
        "inputs": inputs,
        "parameters": {
            "top_p": configs.top_p,
            "temperature": configs.temperature,
            "max_new_tokens": configs.max_tokens,
            "top_k": configs.top_k,
        },
    }
    return payload


class HuggingFaceInferenceEndpointChatCompletionModel(BaseChatCompletionModel):
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
        api_url = credentials.HUGGING_INFERENCE_ENDPOINT_URL
        headers = _build_hugging_face_header(credentials)
        payload = _build_hugging_face_text_generation_payload(messages, stream, provider_model_id, configs)
        return api_url, headers, payload

    # ------------------- handle non-stream chat completion response -------------------

    def extract_core_data(self, response_data: Dict, **kwargs) -> Optional[Dict]:
        return response_data[0]

    def extract_text_content(self, data: Dict, **kwargs) -> Optional[str]:
        message = data.get("generated_text")
        if message is None:
            return None
        return message.split("Answer: ")[-1]

    def extract_function_calls(self, data: Dict, **kwargs) -> Optional[List[ChatCompletionFunctionCall]]:
        pass

    def extract_finish_reason(self, data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        return ChatCompletionFinishReason.unknown

    # ------------------- handle stream chat completion response -------------------

    def stream_check_error(self, sse_data: Dict, **kwargs):
        pass

    def stream_extract_chunk_data(self, sse_data: Dict, **kwargs) -> Optional[Dict]:
        pass

    def stream_extract_chunk(
        self, index: int, chunk_data: Dict, text_content: str, **kwargs
    ) -> Tuple[int, Optional[ChatCompletionChunk]]:
        pass

    def stream_extract_finish_reason(self, chunk_data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        pass

    def stream_handle_function_calls(
        self, chunk_data: Dict, function_calls_content: ChatCompletionFunctionCallsContent, **kwargs
    ) -> Optional[ChatCompletionFunctionCallsContent]:
        pass
