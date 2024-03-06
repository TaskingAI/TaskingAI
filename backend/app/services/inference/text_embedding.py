import aiohttp
from typing import List, Dict, Optional
from tkhelper.utils import ResponseWrapper
from app.config import CONFIG


__all__ = [
    "text_embedding",
]


# For POST /v1/text_embedding
async def text_embedding(
    model_schema_id: str,
    provider_model_id: Optional[str],
    encrypted_credentials: Dict,
    properties: Optional[Dict],
    input_text_list: List[str],
    input_type: Optional[str],
) -> ResponseWrapper:
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
