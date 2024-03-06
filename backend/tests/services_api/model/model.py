import aiohttp
from typing import Dict

from tests.common.utils import ResponseWrapper, get_headers, Token
from tests.settings import HOST, WEB_SERVICE_PORT
from app.config import CONFIG

BASE_URL = f"{HOST}:{WEB_SERVICE_PORT}{CONFIG.WEB_ROUTE_PREFIX}"


async def list_models(data: Dict = None):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/models"
        response = await session.get(request_url, params=data)
        return ResponseWrapper(response.status, await response.json())


async def get_model(model_id: str):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/models/{model_id}"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def create_model(data: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/models"
        response = await session.post(request_url, json=data)
        return ResponseWrapper(response.status, await response.json())


async def update_model(model_id: str, data: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/models/{model_id}"
        response = await session.post(request_url, json=data)
        return ResponseWrapper(response.status, await response.json())


async def delete_model(model_id: str):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/models/{model_id}"
        response = await session.delete(request_url)
        return ResponseWrapper(response.status, await response.json())
