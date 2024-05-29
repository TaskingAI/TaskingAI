import json

from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class ImageSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        SERPER_API_KEY: str = credentials.credentials.get("SERPER_API_KEY")

        url = "https://google.serper.dev/images"

        headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}

        payload = json.dumps({"q": query, "num": 10})

        async with ClientSession() as session:
            async with session.post(url, headers=headers, data=payload, proxy=CONFIG.PROXY) as response:
                if response.status != 200:
                    raise_provider_api_error(await response.text())
                data = await response.json()
                result = {}
                if "images" in data:
                    result["organic_images_results"] = []
                    for item in data["images"]:
                        result["organic_images_results"].append(
                            {
                                "title": item.get("title", ""),
                                "imageUrl": item.get("imageUrl", ""),
                                "source": item.get("link", ""),
                            }
                        )
                return PluginOutput(data={"result": json.dumps(result)})
