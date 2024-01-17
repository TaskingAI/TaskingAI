import aiohttp
from typing import Dict

from tests.common.utils import ResponseWrapper, get_headers, Token
from tests.config import HOST
from config import CONFIG

APP_BASE_URL = f"{HOST}:{CONFIG.SERVICE_PORT}{CONFIG.APP_ROUTE_PREFIX}"


async def list_chats(assistant_id: str, params: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{APP_BASE_URL}/assistants/{assistant_id}/chats"
        response = await session.get(request_url, params=params)
        return ResponseWrapper(response.status, await response.json())


async def get_chat(assistant_id: str, chat_id: str):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{APP_BASE_URL}/assistants/{assistant_id}/chats/{chat_id}"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def create_chat(assistant_id: str, payload: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{APP_BASE_URL}/assistants/{assistant_id}/chats"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def update_chat(assistant_id: str, chat_id: str, payload: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{APP_BASE_URL}/assistants/{assistant_id}/chats/{chat_id}"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def delete_chat(assistant_id: str, chat_id: str):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{APP_BASE_URL}/assistants/{assistant_id}/chats/{chat_id}"
        response = await session.delete(request_url)
        return ResponseWrapper(response.status, await response.json())
