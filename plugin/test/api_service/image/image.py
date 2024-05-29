import aiohttp
from typing import Dict
from test.utils.utils import ResponseWrapper


BASE_URL = "http://localhost:8000/v1/execute"


async def execute(payload: Dict):
    async with aiohttp.ClientSession() as session:
        response = await session.post(BASE_URL, json=payload)
        return ResponseWrapper(response.status, await response.json())
