import aiohttp

from typing import Dict
from backend.tests.common.utils import ResponseWrapper, get_headers
from backend.tests.common.config import CONFIG

ADMIN_BASE_URL = f"{CONFIG.WEB_BASE_URL}/admins"


async def login(payload: Dict):
    async with aiohttp.ClientSession() as session:
        request_url = f"{ADMIN_BASE_URL}/login"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def verify_token(token: str):
    headers = get_headers(token)
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await session.post(f"{ADMIN_BASE_URL}/verify_token")
        return ResponseWrapper(response.status, await response.json())


async def refresh_token(token: str):
    headers = get_headers(token)
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await session.post(f"{ADMIN_BASE_URL}/refresh_token")
        return ResponseWrapper(response.status, await response.json())


async def logout(token: str):
    headers = get_headers(token)
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await session.post(f"{ADMIN_BASE_URL}/logout")
        return ResponseWrapper(response.status, await response.json())
