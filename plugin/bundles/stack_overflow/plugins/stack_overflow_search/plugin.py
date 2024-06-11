import json

from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class StackOverflowSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        tagged: str = plugin_input.input_params.get("tagged", None)
        not_tagged: str = plugin_input.input_params.get("not_tagged", None)
        title: str = plugin_input.input_params.get("title", None)
        sort: str = plugin_input.input_params.get("sort", None)
        order: str = plugin_input.input_params.get("order", None)

        url = f"https://api.stackexchange.com/2.3/search?site=stackoverflow"

        if tagged:
            url += f"&tagged={tagged}"

        if not_tagged:
            url += f"&nottagged={not_tagged}"

        if title:
            url += f"&intitle={title}"

        if sort:
            url += f"&sort={sort}"

        if order:
            url += f"&order={order}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("items")
                    refined_items = []

                    for item in items:
                        refined_item = {
                            "title": item["title"],
                            "link": item["link"],
                            "tags": item["tags"],
                        }
                        refined_items.append(refined_item)

                    return PluginOutput(data={"results": json.dumps(refined_items)})

                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
