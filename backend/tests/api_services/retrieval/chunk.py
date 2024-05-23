import aiohttp
from typing import Dict
from backend.tests.common.utils import ResponseWrapper, get_headers
from backend.tests.common.config import CONFIG
from backend.tests.api_services.retrieval.collection import COLLECTION_BASE_URL

async def query_chunks(collection_id: str, payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{COLLECTION_BASE_URL}/{collection_id}/chunks/query"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def list_record_chunks(collection_id: str, record_id: str, payload: Dict = None):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{COLLECTION_BASE_URL}/{collection_id}/records/{record_id}/chunks"
        response = await session.get(request_url, params=payload)
        return ResponseWrapper(response.status, await response.json())


async def list_collection_chunks(collection_id: str, payload: Dict = None):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{COLLECTION_BASE_URL}/{collection_id}/chunks"
        response = await session.get(request_url, params=payload)
        return ResponseWrapper(response.status, await response.json())


async def create_chunk(collection_id: str, data: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{COLLECTION_BASE_URL}/{collection_id}/chunks"
        response = await session.post(request_url, json=data)
        return ResponseWrapper(response.status, await response.json())


async def get_chunk(collection_id: str, chunk_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{COLLECTION_BASE_URL}/{collection_id}/chunks/{chunk_id}"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def update_chunk(collection_id: str, chunk_id: str, data: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{COLLECTION_BASE_URL}/{collection_id}/chunks/{chunk_id}"
        response = await session.post(request_url, json=data)
        return ResponseWrapper(response.status, await response.json())


async def delete_chunk(collection_id: str, chunk_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{COLLECTION_BASE_URL}/{collection_id}/chunks/{chunk_id}"
        response = await session.delete(request_url)
        return ResponseWrapper(response.status, await response.json())
