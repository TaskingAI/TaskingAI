import json

from aiohttp import ClientSession

import base64
from app.service.image_storage import save_url_image_to_s3_or_local

from bundle_dependency import *
from config import CONFIG


class GenerateImage(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        prompt: str = plugin_input.input_params.get("prompt")
        openai_api_key: str = credentials.credentials.get("OPENAI_API_KEY")
        project_id: str = plugin_input.project_id

        if not project_id:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "project_id is required")

        url = "https://api.openai.com/v1/images/generations"
        headers = {"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"}

        data = {"prompt": prompt, "model": "dall-e-3", "n": 1}

        async with ClientSession() as session:
            async with session.post(url=url, headers=headers, json=data, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data["data"][0]["url"]
                    image_format = "png"
                    image_url = await save_url_image_to_s3_or_local(
                        image_url=image_url,
                        project_id=project_id,
                        file_format=image_format,
                        plugin_id="dalle_3/generate_image",
                    )
                    return PluginOutput(data={"url": image_url})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
