import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class TopStoriesSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        section: str = plugin_input.input_params.get("section")
        new_york_times_api_key: str = credentials.credentials.get("NEW_YORK_TIMES_API_KEY")

        url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={new_york_times_api_key}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("results", [])
                    optimized_items = []
                    for item in items:
                        optimized_items.append(
                            {
                                "title": item.get("title"),
                                "link": item.get("url"),
                                "description": item.get("abstract"),
                            }
                        )
                    return PluginOutput(data={"results": json.dumps(optimized_items)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
