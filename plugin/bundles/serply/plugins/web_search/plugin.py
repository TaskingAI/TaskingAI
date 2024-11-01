import json
from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class WebSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")

        serply_api_key: str = credentials.credentials.get("SERPLY_API_KEY")

        api_url = f"https://api.serply.io/v1/search/q={query}"

        headers = {"Content-Type": "application/json", "X-Api-Key": serply_api_key}

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("results", [])
                    optimized_results = []
                    for result in results:
                        optimized_results.append(
                            {
                                "title": result.get("title"),
                                "url": result.get("link"),
                                "description": result.get("description"),
                            }
                        )
                    return PluginOutput(data={"result": json.dumps(optimized_results)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
