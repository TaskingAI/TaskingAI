import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GetTopHeadlines(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        country: str = plugin_input.input_params.get("country")
        category: str = plugin_input.input_params.get("category")
        count: int = plugin_input.input_params.get("count", 10)

        news_api_key: str = credentials.credentials.get("NEWS_API_API_KEY")

        url = (
            f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={news_api_key}&pageSize={count}&page=1"
            + (f"&category={category}" if category else "")
        )

        if category is not None and category not in [
            "business",
            "entertainment",
            "general",
            "health",
            "science",
            "sports",
            "technology",
        ]:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid category")

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"result": json.dumps(data["articles"])})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
