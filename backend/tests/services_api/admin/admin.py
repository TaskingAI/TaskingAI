import aiohttp

from typing import Dict
from tests.common.utils import ResponseWrapper, get_headers
from tests.settings import HOST, WEB_SERVICE_PORT
from app.config import CONFIG

BASE_URL = f"{HOST}:{WEB_SERVICE_PORT}{CONFIG.WEB_ROUTE_PREFIX}"


async def login(payload: Dict):
    async with aiohttp.ClientSession() as session:
        request_url = f"{BASE_URL}/admins/login"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def verify_token(token: str):
    headers = get_headers(token)
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await session.post(f"{BASE_URL}/admins/verify_token")
        return ResponseWrapper(response.status, await response.json())


async def refresh_token(token: str):
    headers = get_headers(token)
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await session.post(f"{BASE_URL}/admins/refresh_token")
        return ResponseWrapper(response.status, await response.json())


async def logout(token: str):
    headers = get_headers(token)
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await session.post(f"{BASE_URL}/admins/logout")
        return ResponseWrapper(response.status, await response.json())
