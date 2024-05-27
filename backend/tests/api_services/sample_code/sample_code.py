import aiohttp
from typing import Dict

from backend.tests.common.utils import ResponseWrapper, get_headers
from backend.tests.common.config import CONFIG

GET_CODE_URL = f"{CONFIG.BASE_URL}/ui/template_codes/get_code"


async def get_sample_code(payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = GET_CODE_URL
        response = await session.get(request_url, params=payload)
        return ResponseWrapper(response.status, await response.json())
