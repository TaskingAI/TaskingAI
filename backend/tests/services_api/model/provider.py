import aiohttp
from tests.common.utils import ResponseWrapper, get_headers, Token
from tests.settings import HOST, WEB_SERVICE_PORT
from app.config import CONFIG

BASE_URL = f"{HOST}:{WEB_SERVICE_PORT}{CONFIG.WEB_ROUTE_PREFIX}"


async def list_providers():
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/providers"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def get_provider(params: dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/providers/get"
        response = await session.get(request_url, params=params)
        return ResponseWrapper(response.status, await response.json())
