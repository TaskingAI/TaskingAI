import json
from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class ScholarSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")

        serply_api_key: str = credentials.credentials.get("SERPLY_API_KEY")

        api_url = f"https://api.serply.io/v1/scholar/q={query}"

        headers = {"Content-Type": "application/json", "X-Api-Key": serply_api_key}

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    articles = data.get("articles", [])
                    optimized_articles = []
                    for article in articles:
                        optimized_articles.append(
                            {
                                "title": article.get("title"),
                                "url": article.get("link"),
                                "author": article.get("author"),
                                "description": article.get("description"),
                            }
                        )
                    return PluginOutput(data={"result": json.dumps(optimized_articles)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
