import aiohttp
from typing import Dict
from common.utils import ResponseWrapper
from config import CONFIG


async def verify_credentials(
    provider_id: str, provider_model_id: str, model_type: str, credentials: Dict
) -> ResponseWrapper:
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/verify_credentials",
            json={
                "provider_id": provider_id,
                "provider_model_id": provider_model_id,
                "model_type": model_type,
                "credentials": credentials,
            },
        )
        return ResponseWrapper(response.status, await response.json())
