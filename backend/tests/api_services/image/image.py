import aiohttp
from typing import Dict
from backend.tests.common.utils import ResponseWrapper, get_headers, get_file_name
from backend.tests.common.config import CONFIG

IMAGE_BASE_URL = f"{CONFIG.BASE_URL}/images"


async def upload_image(payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        image_path = payload.get("image")
        image_name = get_file_name(image_path)
        data = aiohttp.FormData()
        data.add_field("image", open(image_path, "rb"), filename=image_name, content_type="application/octet-stream")
        for key, value in payload.items():
            if key != "image":
                data.add_field(key, value)
        request_url = IMAGE_BASE_URL
        response = await session.post(request_url, data=data)
        return ResponseWrapper(response.status, await response.json())


async def download_image(url: str):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        return ResponseWrapper(response.status, await response.read())
