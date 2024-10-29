import json
from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class ImageSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        count: int = plugin_input.input_params.get("count", None)
        safe_search: str = plugin_input.input_params.get("safe_search", None)
        brave_api_key: str = credentials.credentials.get("BRAVE_API_KEY")

        api_url = f"https://api.search.brave.com/res/v1/images/search?q={query}"

        if count:
            api_url += f"&count={count}"
        if safe_search:
            api_url += f"&safesearch={safe_search}"

        headers = {"Accept": "application/json", "Accept-Encoding": "gzip", "X-Subscription-Token": brave_api_key}

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("results")
                    optimized_result = []
                    for result in results:
                        optimized_result.append(
                            {"title": result["title"], "url": result["url"], "source": result["source"]}
                        )
                    return PluginOutput(data={"result": json.dumps(optimized_result)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
