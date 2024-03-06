import aiohttp
from typing import Dict

from tests.common.utils import ResponseWrapper, get_headers, Token
from tests.settings import HOST, WEB_SERVICE_PORT
from app.config import CONFIG

BASE_URL = f"{HOST}:{WEB_SERVICE_PORT}{CONFIG.WEB_ROUTE_PREFIX}"


async def list_model_schemas(data: Dict = None):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/model_schemas"
        response = await session.get(request_url, params=data)
        return ResponseWrapper(response.status, await response.json())


async def get_model_schema(data: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/model_schemas/get"
        response = await session.get(request_url, params=data)
        return ResponseWrapper(response.status, await response.json())
