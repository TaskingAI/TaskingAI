import aiohttp
from typing import Dict
from test.utils.utils import ResponseWrapper
from test.setting import Config


async def chat_completion(data: Dict):
    async with aiohttp.ClientSession() as session:
        request_url = f"{Config.BASE_URL}/chat_completion"
        response = await session.post(request_url, json=data)
        return ResponseWrapper(response.status, await response.json())


async def text_embedding(data: Dict):
    async with aiohttp.ClientSession() as session:
        request_url = f"{Config.BASE_URL}/text_embedding"
        response = await session.post(request_url, json=data)
        return ResponseWrapper(response.status, await response.json())


async def rerank(data: Dict):
    async with aiohttp.ClientSession() as session:
        request_url = f"{Config.BASE_URL}/rerank"
        response = await session.post(request_url, json=data)
        return ResponseWrapper(response.status, await response.json())


async def verify_credentials(data: Dict):
    async with aiohttp.ClientSession() as session:
        request_url = f"{Config.BASE_URL}/verify_credentials"
        response = await session.post(request_url, json=data)
        return ResponseWrapper(response.status, await response.json())


async def caches():
    async with aiohttp.ClientSession() as session:
        request_url = f"{Config.BASE_URL}/caches"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def cache_checksums():
    async with aiohttp.ClientSession() as session:
        request_url = f"{Config.BASE_URL}/cache_checksums"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def list_providers():
    async with aiohttp.ClientSession() as session:
        request_url = f"{Config.BASE_URL}/providers"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def get_provider(data: Dict):
    async with aiohttp.ClientSession() as session:
        request_url = f"{Config.BASE_URL}/providers/get"
        response = await session.get(request_url, params=data)
        return ResponseWrapper(response.status, await response.json())


async def get_provider_icon(provider_svg: str):
    async with aiohttp.ClientSession() as session:
        request_url = f"{Config.IMAGE_BASE_URL}/images/providers/icons/{provider_svg}"
        response = await session.get(request_url)
        return response


async def list_model_schemas():
    async with aiohttp.ClientSession() as session:
        request_url = f"{Config.BASE_URL}/model_schemas"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def get_model_schema(data: Dict):
    async with aiohttp.ClientSession() as session:
        request_url = f"{Config.BASE_URL}/model_schemas/get"
        response = await session.get(request_url, params=data)
        return ResponseWrapper(response.status, await response.json())


async def model_property_schemas():
    async with aiohttp.ClientSession() as session:
        request_url = f"{Config.BASE_URL}/model_property_schemas/text_embedding"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def get_resources(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        return response
