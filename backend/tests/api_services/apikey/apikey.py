import aiohttp
from typing import Dict
from backend.tests.common.utils import ResponseWrapper, get_headers
from backend.tests.common.config import CONFIG

APIKEY_BASE_URL = f"{CONFIG.WEB_BASE_URL}/apikeys"

async def list_apikey():
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = APIKEY_BASE_URL
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def create_apikey(data: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = APIKEY_BASE_URL
        response = await session.post(request_url, json=data)
        return ResponseWrapper(response.status, await response.json())


async def update_apikey(apikey_id: str, data: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{APIKEY_BASE_URL}/{apikey_id}"
        response = await session.post(request_url, json=data)
        return ResponseWrapper(response.status, await response.json())


async def get_apikey(apikey_id: str, data: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{APIKEY_BASE_URL}/{apikey_id}"
        response = await session.get(request_url, params=data)
        return ResponseWrapper(response.status, await response.json())


async def delete_apikey(apikey_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{APIKEY_BASE_URL}/{apikey_id}"
        response = await session.delete(request_url)
        return ResponseWrapper(response.status, await response.json())
