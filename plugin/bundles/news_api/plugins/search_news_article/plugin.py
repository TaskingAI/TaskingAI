import json

from aiohttp import ClientSession

from bundle_dependency import *
from dateutil import parser
from dateutil.parser import ParserError

from config import CONFIG


class SearchNewsArticle(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        count: int = plugin_input.input_params.get("count", 10)
        from_date: str = plugin_input.input_params.get("from_date", None)
        to_date: str = plugin_input.input_params.get("to_date", None)

        news_api_key: str = credentials.credentials.get("NEWS_API_API_KEY")

        url = (
            f"https://newsapi.org/v2/everything?q={query}&apiKey={news_api_key}&pageSize={count}&page=1"
            + (f"&from={from_date}" if from_date else "")
            + (f"&to={to_date}" if to_date else "")
        )

        # validate if the date is in the correct format
        try:
            if from_date:
                parser.parse(from_date)
            if to_date:
                parser.parse(to_date)
        except ParserError:
            raise_http_error(400, "Invalid date")

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"result": json.dumps(data["articles"])})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
