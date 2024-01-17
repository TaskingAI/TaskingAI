import aiohttp
from typing import Dict
from tests.common.utils import ResponseWrapper, get_headers, Token
from tests.config import HOST
from config import CONFIG

APP_BASE_URL = f"{HOST}:{CONFIG.SERVICE_PORT}{CONFIG.APP_ROUTE_PREFIX}"


async def query_chunks(collection_id: str, payload: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{APP_BASE_URL}/collections/{collection_id}/chunks/query"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())
