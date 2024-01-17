import aiohttp
from typing import List, Dict, Optional
from common.utils import ResponseWrapper
from config import CONFIG


async def text_embedding(
    provider_id: str,
    provider_model_id: str,
    encrypted_credentials: Dict,
    input_text_list: List[str],
    input_type: Optional[str],
) -> ResponseWrapper:
    request_url = f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/text_embedding"
    payload = {
        "provider_id": provider_id,
        "provider_model_id": provider_model_id,
        "encrypted_credentials": encrypted_credentials,
        "input": input_text_list,
    }
    if input_type:
        payload["input_type"] = input_type

    async with aiohttp.ClientSession() as session:
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())
