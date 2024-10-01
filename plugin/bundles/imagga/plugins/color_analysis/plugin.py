import json
import base64

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class ColorAnalysis(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        image_url: str = plugin_input.input_params.get("image_url")
        extract_overall_colors: int = plugin_input.input_params.get("extract_overall_colors", None)
        extract_object_colors: int = plugin_input.input_params.get("extract_object_colors", None)
        overall_count: int = plugin_input.input_params.get("overall_count", None)

        imagga_api_key: str = credentials.credentials.get("IMAGGA_API_KEY")
        imagga_api_secret: str = credentials.credentials.get("IMAGGA_API_SECRET")
        key = f"{imagga_api_key}:{imagga_api_secret}"
        encoded_key = base64.b64encode(key.encode()).decode()

        headers = {"Authorization": f"Basic {encoded_key}"}

        api_url = f"https://api.imagga.com/v2/colors?image_url={image_url}"

        if extract_overall_colors:
            api_url += f"&extract_overall_colors={extract_overall_colors}"

        if extract_object_colors:
            api_url += f"&extract_object_colors={extract_object_colors}"

        if overall_count:
            api_url += f"&overall_count={overall_count}"

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"result": json.dumps(data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
