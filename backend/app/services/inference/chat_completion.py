import aiohttp
from typing import List, Dict, Optional
from tkhelper.utils import ResponseWrapper
from tkhelper.error import raise_http_error, ErrorCode
from app.config import CONFIG
from app.models import ModelSchema, ModelType, Model
import json
import logging

logger = logging.getLogger(__name__)


__all__ = [
    "chat_completion",
    "chat_completion_stream",
]


async def __validate_model(model: Model):
    if not model.is_chat_completion():
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            message=f"Model {model.model_id} is not a chat completion model.",
        )

    model_schema: ModelSchema = model.model_schema()
    if model_schema is None or model_schema.type == ModelType.WILDCARD:
        provider_model_id = model.provider_model_id
        properties = model.properties
    elif model.is_custom_host():
        provider_model_id = model_schema.provider_model_id
        properties = model.properties
    else:
        provider_model_id = model_schema.provider_model_id
        properties = model_schema.properties

    return provider_model_id, properties


# For POST /v1/chat_completion
async def chat_completion(
    model: Model,
    messages: List[Dict],
    encrypted_credentials: Dict,
    configs: Dict,
    function_call: Optional[str] = None,
    functions: Optional[List[Dict]] = None,
) -> ResponseWrapper:
    model_schema_id = model.model_schema_id
    provider_model_id, properties = await __validate_model(model)
    request_url = f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/chat_completion"
    payload = {
        "model_schema_id": model_schema_id,
        "provider_model_id": provider_model_id,
        "messages": messages,  # List of message dicts
        "encrypted_credentials": encrypted_credentials,
        "properties": properties,
        "configs": configs,
        "function_call": function_call,
        "functions": functions,
        "stream": False,
    }

    async with aiohttp.ClientSession() as session:
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def chat_completion_stream(
    model: Model,
    messages: List[Dict],
    encrypted_credentials: Dict,
    configs: Dict,
    function_call: Optional[str] = None,
    functions: Optional[List[Dict]] = None,
):
    model_schema_id = model.model_schema_id
    provider_model_id, properties = await __validate_model(model)
    request_url = f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/chat_completion"
    payload = {
        "model_schema_id": model_schema_id,
        "provider_model_id": provider_model_id,
        "messages": messages,  # List of message dicts
        "encrypted_credentials": encrypted_credentials,
        "properties": properties,
        "configs": configs,
        "function_call": function_call,
        "functions": functions,
        "stream": True,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(request_url, json=payload) as response:
            buffer = ""
            async for line in response.content:
                if line.endswith(b"\n"):
                    buffer += line.decode()
                    if buffer.endswith("\n\n"):
                        lines = buffer.strip().split("\n")
                        event_data = lines[0][len("data: ") :]
                        if event_data != "[DONE]":
                            try:
                                data = json.loads(event_data)
                                yield data
                            except json.decoder.JSONDecodeError:
                                logger.error(f"Failed to parse json: {event_data}")
                                continue
                        buffer = ""
