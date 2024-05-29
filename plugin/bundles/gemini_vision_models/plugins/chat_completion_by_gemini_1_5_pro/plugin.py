import base64
import json
from io import BytesIO

import aiohttp
from PIL import Image
from aiohttp import ClientSession

from app.service.image_load import fetch_image_format, get_image_base64_string
from bundle_dependency import *
from config import CONFIG


class ChatCompletionByGemini15Pro(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        image_url: str = plugin_input.input_params.get("image_url")
        prompt: str = plugin_input.input_params.get("prompt")
        google_gemini_api_key: str = credentials.credentials.get("GOOGLE_GEMINI_API_KEY")

        image_format = await fetch_image_format(image_url)

        headers = {
            "x-goog-api-key": f" {google_gemini_api_key}",
            "Content-Type": "application/json",
        }

        base64_string = await get_image_base64_string(image_url)

        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {"inlineData": {"mimeType": f"image/{image_format}", "data": base64_string}},
                    ],
                }
            ]
        }

        api_version = "v1beta"
        provider_model_id = "gemini-1.5-pro-latest"
        action = "generateContent"
        url = f"https://generativelanguage.googleapis.com/{api_version}/models/{provider_model_id}:{action}"

        async with ClientSession() as session:
            async with session.post(url=url, headers=headers, json=data, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    response_data = await response.json()
                    result = response_data.get("candidates", [])[0].get("content", {}).get("parts", [])[0].get("text")
                    return PluginOutput(data={"result": result})
                else:
                    response_json = await response.json()
                    raise_provider_api_error(json.dumps(response_json))

