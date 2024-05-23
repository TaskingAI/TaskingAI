import aiohttp
from typing import Dict
from backend.tests.common.utils import ResponseWrapper, get_headers
from backend.tests.common.config import CONFIG

BUNDLE_INSTANCE_BASE_URL = f"{CONFIG.BASE_URL}/bundle_instances"
BUNDLE_BASE_URL = f"{CONFIG.BASE_URL}/bundles"
PLUGIN_BASE_URL = f"{CONFIG.BASE_URL}/plugins"

# For GET /{project_id}/bundle_instances
async def list_bundle_instances(params: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = BUNDLE_INSTANCE_BASE_URL
        response = await session.get(request_url, params=params)
        return ResponseWrapper(response.status, await response.json())


# For GET /{project_id}/bundle_instances/{bundle_instance_id}
async def get_bundle_instance(bundle_instance_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BUNDLE_INSTANCE_BASE_URL}/{bundle_instance_id}"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


# For POST /{project_id}/bundle_instances
async def create_bundle_instance(payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = BUNDLE_INSTANCE_BASE_URL
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


# For POST /{project_id}/bundle_instances/{bundle_instance_id}
async def update_bundle_instance(bundle_instance_id: str, payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BUNDLE_INSTANCE_BASE_URL}/{bundle_instance_id}"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


# For DELETE /{project_id}/bundle_instances/{bundle_instance_id}
async def delete_bundle_instance(bundle_instance_id: str):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BUNDLE_INSTANCE_BASE_URL}/{bundle_instance_id}"
        response = await session.delete(request_url)
        return ResponseWrapper(response.status, await response.json())


async def list_bundles(params: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = BUNDLE_BASE_URL
        response = await session.get(request_url, params=params)
        return ResponseWrapper(response.status, await response.json())


async def list_plugins(params: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = PLUGIN_BASE_URL
        response = await session.get(request_url, params=params)
        return ResponseWrapper(response.status, await response.json())
