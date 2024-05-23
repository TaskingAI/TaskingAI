import aiohttp
from backend.tests.common.utils import ResponseWrapper, get_headers
from backend.tests.common.config import CONFIG

PROVIDER_BASE_URL = f"{CONFIG.WEB_BASE_URL}/providers"


async def list_providers(data: dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = PROVIDER_BASE_URL
        response = await session.get(request_url, params=data)
        return ResponseWrapper(response.status, await response.json())


async def get_provider(params: dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{PROVIDER_BASE_URL}/get"
        response = await session.get(request_url, params=params)
        return ResponseWrapper(response.status, await response.json())
