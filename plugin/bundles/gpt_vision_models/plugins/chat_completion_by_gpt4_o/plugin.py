import base64

import aiohttp
from aiohttp import ClientSession

from app.service.image_load import fetch_image_format, image_url_is_on_localhost, get_image_base64_string
from bundle_dependency import *
from config import CONFIG

async def construct_image_data(image_url: str) -> dict:
    if image_url_is_on_localhost(image_url):
        image_format = await fetch_image_format(image_url)
        base64_string = await get_image_base64_string(image_url)

        return {"type": "image_url", "image_url": {"url": f"data:image/{image_format};base64,{base64_string}"}}

    # Normal image url
    if 'http' in image_url:
        return {"type": "image_url", "image_url": {"url": image_url}}

    raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid image url.")

class ChatCompletionByGpt4O(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        image_url: str = plugin_input.input_params.get("image_url")
        prompt: str = plugin_input.input_params.get("prompt")

        openai_api_key: str = credentials.credentials.get("OPENAI_API_KEY")

        headers = {"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"}

        data = {
            # "model": "gpt-4-turbo",
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        await construct_image_data(image_url),
                    ],
                }
            ],
        }

        async with ClientSession() as session:
            async with session.post(
                url="https://api.openai.com/v1/chat/completions", headers=headers, json=data, proxy=CONFIG.PROXY
            ) as response:
                if response.status != 200:
                    raise_provider_api_error(await response.text())

                data = await response.json()
                result = data["choices"][0]["message"]["content"]
                return PluginOutput(data={"result": result})
