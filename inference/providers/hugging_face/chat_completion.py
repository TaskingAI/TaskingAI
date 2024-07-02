from app.models import ModelSchema
from provider_dependency.chat_completion import *
from typing import List, Optional, Dict, Tuple

logger = logging.getLogger(__name__)


def _build_hugging_face_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.HUGGING_FACE_API_KEY}",
        "Content-Type": "application/json",
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
    prompt = _build_hugging_face_text_generation_message(messages)
    logger.debug("prompt: %s", prompt)
    logger.debug("configs.max_tokens: %s", configs.max_tokens)
    payload = {
        "inputs": prompt,
        "parameters": {
            "top_p": configs.top_p,
            "temperature": configs.temperature,
            "max_new_tokens": configs.max_tokens,
            "top_k": configs.top_k,
        },
    }
    return payload


class HuggingFaceChatCompletionModel(BaseChatCompletionModel):
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
        base_url = "https://api-inference.huggingface.co/models/PLACE_HOLDER_MODEL_ID"
        api_url = base_url.replace("PLACE_HOLDER_MODEL_ID", provider_model_id)
        headers = _build_hugging_face_header(credentials)
        if stream:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Hugging Face does not support streaming.")
        if functions:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Hugging Face does not support function calls.")
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
