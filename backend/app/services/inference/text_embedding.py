import aiohttp
from typing import List, Dict, Optional
from tkhelper.utils import ResponseWrapper
from tkhelper.error import raise_http_error, ErrorCode
from app.config import CONFIG
from app.models import ModelSchema, ModelType, Model


__all__ = [
    "text_embedding",
]


async def __validate_model(model: Model):
    if not model.is_text_embedding():
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            message=f"Model {model.model_id} is not a text embedding model.",
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


# For POST /v1/text_embedding
async def text_embedding(
    model: Model,
    encrypted_credentials: Dict,
    input_text_list: List[str],
    input_type: Optional[str],
) -> ResponseWrapper:
    model_schema_id = model.model_schema_id
    provider_model_id, properties = await __validate_model(model)
    request_url = f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/text_embedding"
    payload = {
        "model_schema_id": model_schema_id,
        "provider_model_id": provider_model_id,
        "encrypted_credentials": encrypted_credentials,
        "properties": properties,
        "input": input_text_list,
    }
    if input_type:
        payload["input_type"] = input_type

    async with aiohttp.ClientSession() as session:
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())
