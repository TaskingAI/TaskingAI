import aiohttp
from typing import Dict
from common.utils import ResponseWrapper
from config import CONFIG
from typing import Optional


async def verify_credentials(
    provider_id: str,
    provider_model_id: str,
    model_type: str,
    credentials: Dict,
    properties: Optional[Dict] = None,
) -> ResponseWrapper:
    payload = {
        "provider_id": provider_id,
        "provider_model_id": provider_model_id,
        "model_type": model_type,
        "credentials": credentials,
    }
    if properties is not None:
        payload["properties"] = properties
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/verify_credentials",
            json=payload,
        )
        return ResponseWrapper(response.status, await response.json())


async def health_check() -> ResponseWrapper:
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/health_check",
        )
        return ResponseWrapper(response.status, await response.json())
