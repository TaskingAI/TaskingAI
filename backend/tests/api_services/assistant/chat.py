import aiohttp
from typing import Dict

from backend.tests.common.utils import ResponseWrapper, get_headers
from backend.tests.common.config import CONFIG
from backend.tests.api_services.assistant.assistant import ASSISTANT_BASE_URL


async def list_chats(assistant_id: str, params: Dict = None):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ASSISTANT_BASE_URL}/{assistant_id}/chats"
        response = await session.get(request_url, params=params)
        return ResponseWrapper(response.status, await response.json())


async def get_chat(assistant_id: str, chat_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ASSISTANT_BASE_URL}/{assistant_id}/chats/{chat_id}"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def create_chat(assistant_id: str, payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ASSISTANT_BASE_URL}/{assistant_id}/chats"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def update_chat(assistant_id: str, chat_id: str, payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ASSISTANT_BASE_URL}/{assistant_id}/chats/{chat_id}"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def delete_chat(assistant_id: str, chat_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ASSISTANT_BASE_URL}/{assistant_id}/chats/{chat_id}"
        response = await session.delete(request_url)
        return ResponseWrapper(response.status, await response.json())
