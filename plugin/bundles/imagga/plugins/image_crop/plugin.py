import json
import base64

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class ImageCrop(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        image_url: str = plugin_input.input_params.get("image_url")
        resolution: str = plugin_input.input_params.get("resolution", None)

        imagga_api_key: str = credentials.credentials.get("IMAGGA_API_KEY")
        imagga_api_secret: str = credentials.credentials.get("IMAGGA_API_SECRET")
        key = f"{imagga_api_key}:{imagga_api_secret}"
        encoded_key = base64.b64encode(key.encode()).decode()

        headers = {"Authorization": f"Basic {encoded_key}"}

        api_url = f"https://api.imagga.com/v2/croppings?image_url={image_url}"

        if resolution:
            api_url += f"&resolution={resolution}"

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    croppings = data.get("result", {}).get("croppings", [])
                    result = []
                    for cropping in croppings:
                        result.append(
                            {
                                "target-height": cropping.get("target_height", None),
                                "target-width": cropping.get("target_width", None),
                                "top-left-coordinates": f"x1: {cropping.get('x1', None)}, y1: {cropping.get('y1', None)}",
                                "bottom-right-coordinates": f"x2: {cropping.get('x2', None)}, y2: {cropping.get('y2', None)}",
                            }
                        )
                    return PluginOutput(data={"result": json.dumps(result)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
