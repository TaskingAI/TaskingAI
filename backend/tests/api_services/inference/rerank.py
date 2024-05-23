import aiohttp
from typing import Dict

from backend.tests.common.utils import ResponseWrapper, get_headers
from backend.tests.common.config import CONFIG

INFERENCE_BASE_URL = f"{CONFIG.BASE_URL}/inference"


async def rerank(params: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{INFERENCE_BASE_URL}/rerank"
        response = await session.post(request_url, json=params)
        return ResponseWrapper(response.status, await response.json())
