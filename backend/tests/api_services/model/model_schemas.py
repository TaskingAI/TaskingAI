import aiohttp
from typing import Dict

from backend.tests.common.utils import ResponseWrapper, get_headers
from backend.tests.common.config import CONFIG

MODEL_SCHEMA_BASE_URL = f"{CONFIG.WEB_BASE_URL}/model_schemas"


async def list_model_schemas(data: Dict = None):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = MODEL_SCHEMA_BASE_URL
        response = await session.get(request_url, params=data)
        return ResponseWrapper(response.status, await response.json())


async def get_model_schema(data: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{MODEL_SCHEMA_BASE_URL}/get"
        response = await session.get(request_url, params=data)
        return ResponseWrapper(response.status, await response.json())
