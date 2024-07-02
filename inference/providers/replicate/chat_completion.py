import asyncio

from app.models import ModelSchema
from provider_dependency.chat_completion import *
from app.models.tokenizer import estimate_input_tokens, estimate_response_tokens
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


def _build_replicate_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Token {credentials.REPLICATE_API_KEY}",
        "Content-Type": "application/json",
    }


def _build_replicate_message(messages: List[ChatCompletionMessage]):
    # Generate "Human" and "Assistant" dialogue parts
    prompt_parts = []
    for msg in messages:
        if msg.role in [ChatCompletionRole.user, ChatCompletionRole.system]:
            prompt_parts.append(f"\n\n[INST]{msg.content}[/INST]")
        elif msg.role == ChatCompletionRole.assistant:
            prompt_parts.append(f"\n\n {msg.content}")
    return "".join(prompt_parts)


def _build_replicate_chat_completion_payload(
    messages: List[ChatCompletionMessage],
    stream: bool,
    provider_model_id: str,
    configs: ChatCompletionModelConfiguration,
):
    # Convert ChatCompletionMessages to the required format
    prompt = _build_replicate_message(messages)
    logger.debug("prompt: %s", prompt)
    logger.debug("configs.max_tokens: %s", configs.max_tokens)
    payload = {
        "input": {
            "prompt": prompt,
        },
        "stream": stream,
    }
    config_dict = configs.model_dump()
    for key, value in config_dict.items():
        if value is not None:
            if key == "max_tokens":
                payload["input"]["max_new_tokens"] = value
            elif key == "stop":
                payload["input"]["stop"] = ",".join(value)
            else:
                payload["input"][key] = value
    return payload


class ReplicateChatCompletionModel(BaseChatCompletionModel):
    API_URL = "https://api.replicate.com/v1/models/PLACE_HOLDER_MODEL_ID/predictions"

    def __init__(self):
        super().__init__()

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
        # Convert ChatCompletionMessages to the required format

        headers = _build_replicate_header(credentials)
        payload = _build_replicate_chat_completion_payload(messages, False, provider_model_id, configs)
        input_tokens = estimate_input_tokens(
            [message.model_dump() for message in messages],
            [function.model_dump() for function in functions] if functions else None,
            function_call,
        )

        if "/" in provider_model_id:
            real_api_url = self.API_URL.replace("PLACE_HOLDER_MODEL_ID", provider_model_id)
        else:
            real_api_url = "https://api.replicate.com/v1/predictions"
            payload["version"] = provider_model_id
        if proxy:
            if not proxy.startswith("https://"):
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid proxy URL. Must start with https://")
            # replace the base url with the proxy
            real_api_url = proxy

        if custom_headers:
            headers.update(custom_headers)
        logger.debug("headers = %s", headers)
        logger.debug("payload = %s", payload)
        async with aiohttp.ClientSession() as session:
            async with session.post(real_api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                result = await response.json()
                if response.status != 201:
                    raise_http_error(
                        ErrorCode.PROVIDER_ERROR,
                        f"Error on calling provider model API: " f"{result}",
                    )

                result_url = result["urls"]["get"]

                logger.debug(f"result_url = {result_url}")

                get_result_response = await session.get(result_url, headers=headers, proxy=CONFIG.PROXY)

                result_response_data = await get_result_response.json()
                while result_response_data["status"] != "succeeded":
                    await asyncio.sleep(1)
                    get_result_response = await session.get(result_url, headers=headers, proxy=CONFIG.PROXY)
                    result_response_data = await get_result_response.json()

                output = result_response_data["output"]
                output_concat = "".join(output)

                logger.debug(f"output_concat = {output_concat}")
                finish_reason = ChatCompletionFinishReason.unknown
                message = ChatCompletionAssistantMessage(content=output_concat)

                output_tokens = estimate_response_tokens(message.model_dump())
                response = ChatCompletion(
                    finish_reason=finish_reason,
                    message=message,
                    created_timestamp=get_current_timestamp_int(),
                    usage=ChatCompletionUsage(input_tokens=input_tokens, output_tokens=output_tokens),
                )

                logger.debug(f"response = {response}")
                logger.debug(f"response.message = {response.message}")
                logger.debug(f"response.message.content = {response.message.content}")
                logger.debug(f"response.finish_reason = {response.finish_reason}")
                return response

    async def chat_completion_stream(
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
        pass
