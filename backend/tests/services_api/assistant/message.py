import aiohttp
from typing import Dict

from tests.common.utils import ResponseWrapper, get_headers, Token
from tests.settings import HOST
from app.config import CONFIG

if CONFIG.WEB:
    BASE_URL = f"{HOST}:{CONFIG.SERVICE_PORT}{CONFIG.WEB_ROUTE_PREFIX}"
elif CONFIG.API:
    BASE_URL = f"{HOST}:{CONFIG.SERVICE_PORT}{CONFIG.API_ROUTE_PREFIX}"
    from tests.common.utils import APIKEY

    Token = APIKEY


async def create_message(assistant_id: str, chat_id: str, payload: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/assistants/{assistant_id}/chats/{chat_id}/messages"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def list_messages(assistant_id: str, chat_id: str, payload: Dict = None):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/assistants/{assistant_id}/chats/{chat_id}/messages"
        response = await session.get(url=request_url, params=payload)
        return ResponseWrapper(response.status, await response.json())


async def get_message(assistant_id: str, chat_id: str, message_id: str):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/assistants/{assistant_id}/chats/{chat_id}/messages/{message_id}"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def update_message(assistant_id: str, chat_id: str, message_id: str, payload: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/assistants/{assistant_id}/chats/{chat_id}/messages/{message_id}"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def generate_message(assistant_id: str, chat_id: str, payload: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/assistants/{assistant_id}/chats/{chat_id}/generate"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())
