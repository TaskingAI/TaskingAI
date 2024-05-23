import aiohttp
from typing import Dict

from backend.tests.common.utils import ResponseWrapper, get_headers
from backend.tests.common.config import CONFIG

MODEL_BASE_URL = f"{CONFIG.WEB_BASE_URL}/models"


async def list_models(data: Dict = None):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = MODEL_BASE_URL
        response = await session.get(request_url, params=data)
        return ResponseWrapper(response.status, await response.json())


async def get_model(model_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{MODEL_BASE_URL}/{model_id}"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def create_model(data: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = MODEL_BASE_URL
        response = await session.post(request_url, json=data)
        return ResponseWrapper(response.status, await response.json())


async def update_model(model_id: str, data: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{MODEL_BASE_URL}/{model_id}"
        response = await session.post(request_url, json=data)
        return ResponseWrapper(response.status, await response.json())


async def delete_model(model_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{MODEL_BASE_URL}/{model_id}"
        response = await session.delete(request_url)
        return ResponseWrapper(response.status, await response.json())
