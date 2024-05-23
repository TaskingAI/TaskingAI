import aiohttp
from typing import Dict

from backend.tests.common.utils import ResponseWrapper, get_headers
from backend.tests.common.config import CONFIG

ACTION_BASE_URL = f"{CONFIG.BASE_URL}/actions"


async def list_actions(params: Dict = None):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = ACTION_BASE_URL
        response = await session.get(request_url, params=params)
        return ResponseWrapper(response.status, await response.json())


async def get_action(action_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ACTION_BASE_URL}/{action_id}"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def create_action(payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ACTION_BASE_URL}/bulk_create"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def update_action(action_id: str, payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ACTION_BASE_URL}/{action_id}"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def delete_action(action_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ACTION_BASE_URL}/{action_id}"
        response = await session.delete(request_url)
        return ResponseWrapper(response.status, await response.json())


async def run_action(action_id: str, payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{ACTION_BASE_URL}/{action_id}/run"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())
