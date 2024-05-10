import aiohttp
from typing import Dict
from backend.tests.common.utils import ResponseWrapper, get_headers, get_file_name
from backend.tests.common.config import CONFIG

FILE_BASE_URL = f"{CONFIG.BASE_URL}/files"

async def upload_file(payload: Dict):
    headers = get_headers(CONFIG.Authentication)
    async with aiohttp.ClientSession(headers=headers) as session:
        file_path = payload.get('file')
        file_name = get_file_name(file_path)
        data = aiohttp.FormData()
        data.add_field('file',
                       open(file_path, 'rb'),
                       filename=file_name,
                       content_type='application/octet-stream')
        for key, value in payload.items():
            if key != "file":
                data.add_field(key, value)
        request_url = FILE_BASE_URL
        response = await session.post(request_url, data=data)
        return ResponseWrapper(response.status, await response.json())
