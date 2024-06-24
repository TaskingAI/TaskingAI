import json

from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class WikipediaSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        q: str = plugin_input.input_params.get("q")
        limit: str = plugin_input.input_params.get("limit", 10)

        url = f"https://en.wikipedia.org/w/rest.php/v1/search/page?q={q}&limit={limit}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    pages = data.get("pages", [])
                    optimized_items = []
                    for page in pages:
                        optimized_items.append(
                            {"title": page["title"], "description": page["description"], "excerpt": page["excerpt"]}
                        )
                    return PluginOutput(data={"results": json.dumps(optimized_items)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
