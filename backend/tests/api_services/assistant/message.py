import aiohttp
from typing import Dict

from backend.tests.common.utils import ResponseWrapper, get_headers
from backend.tests.common.config import CONFIG
from backend.tests.api_services.assistant.assistant import ASSISTANT_BASE_URL

async def create_message(assistant_id: str,  chat_id: str, payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ASSISTANT_BASE_URL}/{assistant_id}/chats/{chat_id}/messages"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def list_messages(assistant_id: str, chat_id: str, payload: Dict = None):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ASSISTANT_BASE_URL}/{assistant_id}/chats/{chat_id}/messages"
        response = await session.get(url=request_url,  params=payload)
        return ResponseWrapper(response.status, await response.json())


async def get_message(assistant_id: str, chat_id: str, message_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ASSISTANT_BASE_URL}/{assistant_id}/chats/{chat_id}/messages/{message_id}"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def update_message(assistant_id: str, chat_id: str, message_id: str, payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ASSISTANT_BASE_URL}/{assistant_id}/chats/{chat_id}/messages/{message_id}"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def generate_message(assistant_id: str, chat_id: str, payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ASSISTANT_BASE_URL}/{assistant_id}/chats/{chat_id}/generate"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())
