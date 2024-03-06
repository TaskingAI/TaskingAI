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


async def query_chunks(collection_id: str, payload: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/collections/{collection_id}/chunks/query"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def list_record_chunks(collection_id: str, record_id: str, payload: Dict = None):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/collections/{collection_id}/records/{record_id}/chunks"
        response = await session.get(request_url, params=payload)
        return ResponseWrapper(response.status, await response.json())


async def list_collection_chunks(collection_id: str, payload: Dict = None):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/collections/{collection_id}/chunks"
        response = await session.get(request_url, params=payload)
        return ResponseWrapper(response.status, await response.json())


async def create_chunk(collection_id: str, data: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/collections/{collection_id}/chunks"
        response = await session.post(request_url, json=data)
        return ResponseWrapper(response.status, await response.json())


async def get_chunk(collection_id: str, chunk_id: str):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/collections/{collection_id}/chunks/{chunk_id}"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def update_chunk(collection_id: str, chunk_id: str, data: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/collections/{collection_id}/chunks/{chunk_id}"
        response = await session.post(request_url, json=data)
        return ResponseWrapper(response.status, await response.json())


async def delete_chunk(collection_id: str, chunk_id: str):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/collections/{collection_id}/chunks/{chunk_id}"
        response = await session.delete(request_url)
        return ResponseWrapper(response.status, await response.json())
