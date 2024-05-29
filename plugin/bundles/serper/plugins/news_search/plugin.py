import json

from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class NewsSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        SERPER_API_KEY: str = credentials.credentials.get("SERPER_API_KEY")

        url = "https://google.serper.dev/news"

        headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}

        payload = json.dumps({"q": query, "num": 10})

        async with ClientSession() as session:
            async with session.post(url, headers=headers, data=payload, proxy=CONFIG.PROXY) as response:
                if response.status != 200:
                    raise_provider_api_error(await response.text())
                data = await response.json()
                result = {}
                if "news" in data:
                    result["organic_news_results"] = []
                    for item in data["news"]:
                        result["organic_news_results"].append(
                            {
                                "title": item.get("title", ""),
                                "link": item.get("link", ""),
                                "snippet": item.get("snippet", ""),
                                "date": item.get("date", ""),
                                "source": item.get("source", ""),
                            }
                        )
                return PluginOutput(data={"result": json.dumps(result)})
