import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class WebSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        api_key: str = credentials.credentials.get("GOOGLE_CUSTOM_SEARCH_API_KEY")
        engine_id: str = credentials.credentials.get("GOOGLE_CUSTOM_SEARCH_ENGINE_ID")

        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={engine_id}&q={query}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("items", [])
                    optimized_items = []
                    for item in items:
                        optimized_items.append(
                            {"title": item["title"], "link": item["link"], "description": item["snippet"]}
                        )
                    return PluginOutput(data={"results": json.dumps(optimized_items)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
