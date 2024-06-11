import json

from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class WebSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        api_key: str = credentials.credentials.get("BING_SEARCH_API_KEY")

        url = f"https://api.bing.microsoft.com/v7.0/search?q={query}"

        headers = {"Ocp-Apim-Subscription-Key": api_key}

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    pages = data.get("webPages", [])
                    items = pages.get("value", [])
                    optimized_items = []
                    for item in items:
                        optimized_items.append(
                            {"title": item["name"], "link": item["url"], "description": item["snippet"]}
                        )
                    return PluginOutput(data={"results": json.dumps(optimized_items)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
