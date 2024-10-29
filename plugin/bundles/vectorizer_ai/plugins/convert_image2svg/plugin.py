import json
import base64
from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class ConvertImage2Svg(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        image_url: str = plugin_input.input_params.get("image_url", None)
        image_base64: str = plugin_input.input_params.get("image_base64", None)
        mode: str = plugin_input.input_params.get("mode", None)
        output_size_unit: str = plugin_input.input_params.get("output_size_unit", None)
        output_size_width: float = plugin_input.input_params.get("output_size_width", None)
        output_size_height: float = plugin_input.input_params.get("output_size_height", None)
        vectorizer_api_id: str = credentials.credentials.get("VECTORIZER_API_ID")
        vectorizer_api_secret: str = credentials.credentials.get("VECTORIZER_API_SECRET")

        key = f"{vectorizer_api_id}:{vectorizer_api_secret}"
        encoded_key = base64.b64encode(key.encode("utf-8")).decode("utf-8")
        headers = {"Authorization": f"Basic {encoded_key}"}

        api_url = "https://api.vectorizer.ai/api/v1/vectorize"

        body = {}

        if image_url:
            body["image.url"] = image_url
        else:
            body["image.base64"] = image_base64
        if mode:
            body["mode"] = mode
        if output_size_unit:
            body["output.size.unit"] = output_size_unit
        if output_size_width:
            body["output.size.width"] = output_size_width
        if output_size_height:
            body["output.size.height"] = output_size_height

        async with ClientSession() as session:
            async with session.post(url=api_url, headers=headers, json=body, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.text()
                    return PluginOutput(data={"svg": data})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
