from typing import Tuple, Dict

from app.models import ModelSchema
from provider_dependency.chat_completion import *
from .utils import *

logger = logging.getLogger(__name__)


def _build_ai21_message(message: ChatCompletionMessage):
    if message.role in [
        ChatCompletionRole.user,
        ChatCompletionRole.assistant,
    ] or is_assistant_text_message(message):
        return {"role": message.role.name, "text": message.content}


def _build_ai21_chat_completion_payload(
    messages: List[ChatCompletionMessage],
    stream: bool,
    provider_model_id: str,
    configs: ChatCompletionModelConfiguration,
    function_call: Optional[str],
    functions: Optional[List[ChatCompletionFunction]],
):
    # Convert ChatCompletionMessages to the required format
    formatted_messages = [_build_ai21_message(msg) for msg in messages if msg.role != ChatCompletionRole.system]
    logger.debug("formatted_messages: %s", formatted_messages)
    payload = {"messages": formatted_messages, "numResults": 1}

    system_messages = [msg for msg in messages if msg.role == ChatCompletionRole.system]
    payload["system"] = "" + "".join([msg.content for msg in system_messages])

    config_dict = configs.model_dump()
    for key, value in config_dict.items():
        if key == "temperature" and value is not None:
            payload["temperature"] = value
        elif key == "top_p" and value is not None:
            payload["topP"] = value
        elif key == "max_tokens" and value is not None:
            payload["maxTokens"] = value
        elif key == "stop" and value is not None:
            payload["stopSequences"] = value
        elif key == "top_k" and value is not None:
            payload["topKReturn"] = value

    return payload


class Ai21ChatCompletionModel(BaseChatCompletionModel):
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
        api_url = f"https://api.ai21.com/studio/v1/{provider_model_id}/chat"
        headers = build_ai21_header(credentials)
        payload = _build_ai21_chat_completion_payload(
            messages, stream, provider_model_id, configs, function_call, functions
        )
        return api_url, headers, payload

    # ------------------- handle non-stream chat completion response -------------------

    def extract_core_data(self, response_data: Dict, **kwargs) -> Optional[Dict]:
        if not response_data.get("outputs"):
            return None
        return response_data["outputs"][0]

    def extract_text_content(self, data: Dict, **kwargs) -> Optional[str]:
        message_data = data.get("text")
        return message_data

    def extract_function_calls(self, data: Dict, **kwargs) -> Optional[List[ChatCompletionFunctionCall]]:

        return None

    def extract_finish_reason(self, data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        finish_reason = data.get("finishReason", {}).get("reason", "unknown")
        # only possible values: endoftext, length, stop
        if finish_reason == "endoftext":
            return ChatCompletionFinishReason.stop
        return ChatCompletionFinishReason.__members__.get(finish_reason, ChatCompletionFinishReason.unknown)
