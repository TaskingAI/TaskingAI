import aiohttp
from typing import List, Dict
from tkhelper.utils import ResponseWrapper
from tkhelper.error import raise_http_error, ErrorCode
from app.config import CONFIG
from app.models import ModelSchema, ModelType, Model


__all__ = [
    "rerank",
]


async def __validate_model(model: Model):
    if not model.is_rerank():
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            message=f"Model {model.model_id} is not a rerank model.",
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


# For POST /v1/rerank
async def rerank(
    model: Model,
    encrypted_credentials: Dict,
    query: str,
    documents: List[str],
    top_n: int,
) -> ResponseWrapper:
    model_schema_id = model.model_schema_id
    provider_model_id, properties = await __validate_model(model)
    request_url = f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/rerank"
    payload = {
        "model_schema_id": model_schema_id,
        "provider_model_id": provider_model_id,
        "encrypted_credentials": encrypted_credentials,
        "properties": properties,
        "query": query,
        "documents": documents,
        "top_n": top_n,
    }

    async with aiohttp.ClientSession() as session:
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())
