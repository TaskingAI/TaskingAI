from typing import Dict
from app.models import ProviderCredentials, ModelSchema
from provider_dependency.chat_completion import *
from aiobotocore.session import get_session
import json
from app.models.tokenizer import estimate_input_tokens

logger = logging.getLogger(__name__)


def _build_aws_bedrock_messages(messages: List[ChatCompletionMessage], model_prefix: str) -> str:
    # Define message formats corresponding to different model prefixes
    prefix_map = {
        "anthropic": {"user_prefix": "\n\nHuman:", "user_postfix": "", "assistant_prefix": "\n\nAssistant:"},
        "meta": {"user_prefix": "\n[INST]", "user_postfix": "[\\INST]\n", "assistant_prefix": ""},
        "amazon": {"user_prefix": "\n\nUser:", "user_postfix": "", "assistant_prefix": "\n\nBot:"},
        "default": {"user_prefix": "", "user_postfix": "", "assistant_prefix": ""},
    }

    prefixes = prefix_map.get(model_prefix, prefix_map["default"])

    if not messages or not isinstance(messages[-1], ChatCompletionAssistantMessage):
        messages.append(ChatCompletionAssistantMessage(content=""))

    formatted_messages = []
    for message in messages:
        if isinstance(message, ChatCompletionUserMessage):
            message_text = f"{prefixes['user_prefix']} {message.content} {prefixes['user_postfix']}"
        elif isinstance(message, ChatCompletionAssistantMessage):
            message_text = f"{prefixes['assistant_prefix']} {message.content}"
        elif isinstance(message, ChatCompletionSystemMessage):
            message_text = message.content
        else:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"Unknown message type: {type(message).__name__}")

        formatted_messages.append(message_text)

    # trim off ' '
    text = "".join(formatted_messages).rstrip()
    return text


def _build_aws_bedrock_chat_completion_payload(
    messages: List[ChatCompletionMessage],
    stream: bool,
    provider_model_id: str,
    configs: ChatCompletionModelConfiguration,
):
    model_prefix = provider_model_id.split(".")[0]
    payload = {}
    config_dict = configs.model_dump()

    # Define configuration mappings for different providers
    config_mappings = {
        "amazon": {
            "max_tokens": "maxTokenCount",
            "top_p": "topP",
            "config_key": "textGenerationConfig",
            "input_key": "inputText",
        },
        "ai21": {
            "max_tokens": "maxTokens",
            "stop": "stopSequences",
            "top_k": "topKReturn",
            "top_p": "topP",
            "input_key": "prompt",
        },
        "anthropic": {
            "max_tokens": "max_tokens_to_sample",
            "stop": "stop_sequences",
            "input_key": "prompt",
        },
        "cohere": {
            "top_p": "p",
            "top_k": "k",
            # No input_key needed for Cohere as it's handled separately
        },
        "meta": {
            "max_tokens": "max_gen_len",
            "input_key": "prompt",
        },
    }

    provider_config = config_mappings.get(model_prefix, {})
    config_key = provider_config.get("config_key", None)

    if config_key:
        payload[config_key] = {}
        target_config = payload[config_key]
    else:
        target_config = payload

    # Apply configurations
    for key, value in config_dict.items():
        if value is not None:
            mapped_key = provider_config.get(key, key)
            if key == "stop" and model_prefix in ["ai21", "anthropic"] and isinstance(value, list):
                value = [str(item) for item in value]  # Convert all to strings
            target_config[mapped_key] = value

    # Set the input text, specifically handling Cohere differently
    if model_prefix == "cohere":
        payload["prompt"] = messages[0].content if messages else ""
        payload["stream"] = stream
    else:
        if model_prefix == "anthropic" and not payload.get("max_tokens_to_sample"):
            payload["max_tokens_to_sample"] = 4096
        elif model_prefix == "ai21" and not payload.get("maxTokens"):
            payload["maxTokens"] = 4096
        input_key = provider_config.get("input_key", "prompt")
        payload[input_key] = _build_aws_bedrock_messages(messages, model_prefix)

    return payload


class AwsBedrockChatCompletionModel(BaseChatCompletionModel):
    def __init__(self):
        super().__init__()

    # ------------------- prepare request data -------------------

    async def chat_completion(
        self,
        provider_model_id: str,
        messages: List[ChatCompletionMessage],
        credentials: ProviderCredentials,
        configs: ChatCompletionModelConfiguration,
        function_call: Optional[str] = None,
        functions: Optional[List[ChatCompletionFunction]] = None,
        proxy: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None,
        model_schema: ModelSchema = None,
    ):
        payload = _build_aws_bedrock_chat_completion_payload(messages, False, provider_model_id, configs)
        input_tokens = estimate_input_tokens(
            [message.model_dump() for message in messages],
            [function.model_dump() for function in functions] if functions else None,
            function_call,
        )
        try:
            session = get_session()
            async with session.create_client(
                service_name="bedrock-runtime",
                region_name=credentials.AWS_REGION,
                aws_access_key_id=credentials.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=credentials.AWS_SECRET_ACCESS_KEY,
            ) as runtime_client:
                body_jsonstr = json.dumps(payload)
                response = await runtime_client.invoke_model(
                    modelId=provider_model_id, contentType="application/json", accept="*/*", body=body_jsonstr
                )
                response_content = await response["body"].read()
                result = json.loads(response_content.decode("utf-8"))
                model_prefix = provider_model_id.split(".")[0]
                text_content = self.extract_text_content(result, model_prefix=model_prefix)
                finish_reason = self.extract_finish_reason(result, model_prefix=model_prefix)
                response = self.prepare_response(
                    finish_reason=finish_reason,
                    text_content=text_content,
                    function_calls_content=None,
                    function_calls=None,
                    input_tokens=input_tokens,
                    output_tokens=None,
                )
                return response
        except Exception as e:
            raise_http_error(ErrorCode.PROVIDER_ERROR, f"Error invoking model: {e}")

    # ------------------- handle non-stream chat completion response -------------------

    def extract_text_content(self, data: Dict, **kwargs) -> Optional[str]:
        model_prefix = kwargs.get("model_prefix")
        try:
            if model_prefix == "amazon":
                return data["results"][0]["outputText"].strip("\n")
            elif model_prefix == "ai21":
                return data["completions"][0]["data"]["text"]
            elif model_prefix == "anthropic":
                return data["completion"]
            elif model_prefix == "cohere":
                return data["generations"][0]["text"]
            elif model_prefix == "meta":
                return data["generation"].strip("\n")
        except (KeyError, IndexError):
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR, f"Error extracting text content from model response: {data}"
            )
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, f"Unknown model prefix: {model_prefix}")

    def extract_finish_reason(self, data: Dict, **kwargs) -> Optional[ChatCompletionFinishReason]:
        if "error" in data:
            raise_provider_api_error(data["error"])

        model_prefix = kwargs.get("model_prefix")

        # Define a dictionary mapping model prefixes to parsing logic for completion reasons
        finish_reason_mappings = {
            "amazon": lambda x: ChatCompletionFinishReason.stop
            if x["results"][0]["completionReason"] == "FINISH"
            else ChatCompletionFinishReason.length
            if x["results"][0]["completionReason"] == "LENGTH"
            else ChatCompletionFinishReason.unknown,
            "ai21": lambda x: ChatCompletionFinishReason.stop
            if x["completions"][0]["finishReason"]["reason"] == "endoftext"
            or x["completions"][0]["finishReason"]["reason"] == "stop"
            else ChatCompletionFinishReason.length
            if x["completions"][0]["finishReason"]["reason"] == "max_tokens"
            or x["completions"][0]["finishReason"]["reason"] == "length"
            else ChatCompletionFinishReason.unknown,
            "anthropic": lambda x: ChatCompletionFinishReason.stop
            if x["stop_reason"] == "stop_sequence"
            else ChatCompletionFinishReason.length
            if x["stop_reason"] == "max_tokens"
            else ChatCompletionFinishReason.unknown,
            "cohere": lambda x: ChatCompletionFinishReason.stop
            if x["generations"][0]["finish_reason"] == "COMPLETE"
            else ChatCompletionFinishReason.length
            if x["generations"][0]["finish_reason"] == "MAX_TOKENS"
            else ChatCompletionFinishReason.unknown,
            "meta": lambda x: ChatCompletionFinishReason.length
            if x["stop_reason"] == "length"
            else ChatCompletionFinishReason.stop
            if x["stop_reason"] == "stop"
            else ChatCompletionFinishReason.unknown,
        }

        if model_prefix in finish_reason_mappings:
            return finish_reason_mappings[model_prefix](data)
        else:
            raise_http_error(ErrorCode.OBJECT_NOT_FOUND, f"Unknown model prefix: {model_prefix}")

    # ------------------- handle stream chat completion response -------------------
