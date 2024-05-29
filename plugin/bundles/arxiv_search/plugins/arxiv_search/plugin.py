import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG
import xmltodict


class ArxivSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        max_results: int = (
            plugin_input.input_params.get("max_results") if plugin_input.input_params.get("max_results") else 5
        )

        url = f"http://export.arxiv.org/api/query?search_query={query}&max_results={max_results}"
        headers = {"accept": "application/json", "content-type": "application/json"}
        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY, headers=headers) as response:
                if response.status == 200:
                    data = await response.text()
                    data_in_json = xmltodict.parse(data)
                    filtered_data = data_in_json["feed"]["entry"]
                    final_data = [
                        {
                            "id": entry["id"],
                            "title": entry["title"],
                            "summary": entry["summary"],
                            "published": entry["published"],
                            "author": entry["author"],
                            "link": entry["link"],
                        }
                        for entry in filtered_data
                        if isinstance(entry, dict)
                    ]
                    return PluginOutput(data={"results": json.dumps(final_data)})
                else:
                    data = await response.text()
                    raise_provider_api_error(data)
