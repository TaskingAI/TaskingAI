import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class FinanceNewsSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        date: str = plugin_input.input_params.get("date", None)
        keyword: str = plugin_input.input_params.get("keyword", None)
        limit: int = plugin_input.input_params.get("limit", 25)
        source: str = plugin_input.input_params.get("source", None)
        tags: str = plugin_input.input_params.get("tags", None)
        tickers: str = plugin_input.input_params.get("tickers", None)

        finance_news_api_key: str = credentials.credentials.get("FINANCE_NEWS_API_KEY")

        api_url = f"https://api.apilayer.com/financelayer/news?limit={limit}"
        if date:
            api_url += f"&date={date}"
        if keyword:
            api_url += f"&keyword={keyword}"
        if source:
            api_url += f"&source={source}"
        if tags:
            api_url += f"&tags={tags}"
        if tickers:
            api_url += f"&tickers={tickers}"

        headers = {"apikey": finance_news_api_key}

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("data", [])
                    return PluginOutput(data={"results": json.dumps(results)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
