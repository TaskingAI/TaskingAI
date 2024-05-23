import aiohttp
from typing import Dict
from backend.tests.common.utils import ResponseWrapper, get_headers
from backend.tests.common.config import CONFIG
from backend.tests.api_services.retrieval.collection import COLLECTION_BASE_URL


async def list_records(collection_id: str, params: Dict = None):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{COLLECTION_BASE_URL}/{collection_id}/records"
        response = await session.get(request_url, params=params)
        return ResponseWrapper(response.status, await response.json())


async def get_record(collection_id: str, record_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{COLLECTION_BASE_URL}/{collection_id}/records/{record_id}"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def create_record(collection_id: str, payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{COLLECTION_BASE_URL}/{collection_id}/records"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def update_record(collection_id: str, record_id: str, payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{COLLECTION_BASE_URL}/{collection_id}/records/{record_id}"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def delete_record(collection_id: str, record_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{COLLECTION_BASE_URL}/{collection_id}/records/{record_id}"
        response = await session.delete(request_url)
        return ResponseWrapper(response.status, await response.json())
