import json

import aiohttp


from bundle_dependency import *
from config import CONFIG


class SearchVideo(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        GOOGLE_API_KEY: str = credentials.credentials.get("GOOGLE_API_KEY")

        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&key={GOOGLE_API_KEY}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data["items"]
                    refined_items = []

                    for item in items:
                        refined_item = {
                            "title": item["snippet"]["title"],
                            "description": item["snippet"]["description"],
                            "id": item["id"],
                            "publishedAt": item["snippet"]["publishedAt"],
                        }
                        refined_items.append(refined_item)

                    return PluginOutput(data={"result": json.dumps(refined_items)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
