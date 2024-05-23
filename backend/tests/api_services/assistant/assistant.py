import aiohttp
from typing import Dict

from backend.tests.common.utils import ResponseWrapper, get_headers
from backend.tests.common.config import CONFIG

ASSISTANT_BASE_URL = f"{CONFIG.BASE_URL}/assistants"

async def list_assistants(params: Dict = None):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = ASSISTANT_BASE_URL
        response = await session.get(request_url, params=params)
        return ResponseWrapper(response.status, await response.json())


async def list_ui_assistants(params: Dict = None):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        path_list = ASSISTANT_BASE_URL.split('/')
        path_list.insert(-1, 'ui')
        request_url = '/'.join(path_list)
        response = await session.get(request_url, params=params)
        return ResponseWrapper(response.status, await response.json())


async def get_assistant(assistant_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ASSISTANT_BASE_URL}/{assistant_id}"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def get_ui_assistant(assistant_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        path_list = ASSISTANT_BASE_URL.split('/')
        path_list.insert(-1, 'ui')
        base_url = '/'.join(path_list)
        request_url = f"{base_url}/{assistant_id}"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())



async def create_assistant(payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = ASSISTANT_BASE_URL
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def update_assistant(assistant_id: str, payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ASSISTANT_BASE_URL}/{assistant_id}"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def delete_assistant(assistant_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ASSISTANT_BASE_URL}/{assistant_id}"
        response = await session.delete(request_url)
        return ResponseWrapper(response.status, await response.json())
