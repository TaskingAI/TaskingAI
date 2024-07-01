import json

from aiohttp import ClientSession

from datetime import datetime
from bundle_dependency import *
from config import CONFIG


class NewsSearch(PluginHandler):
    def is_valid_yyyymmdd(self, date_str):
        if len(date_str) != 8 or not date_str.isdigit():
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "The date format is incorrect.")
        try:
            datetime.strptime(date_str, "%Y%m%d")
        except ValueError:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "The date format is incorrect.")
        return True

    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query", "")
        begin_date: str = plugin_input.input_params.get("begin_date", "")
        end_date: str = plugin_input.input_params.get("end_date", "")
        new_york_times_api_key: str = credentials.credentials.get("NEW_YORK_TIMES_API_KEY")

        url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={new_york_times_api_key}"

        if begin_date and self.is_valid_yyyymmdd(begin_date):
            url = f"{url}&begin_date={begin_date}"
        if end_date and self.is_valid_yyyymmdd(end_date):
            url = f"{url}&end_date={end_date}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("response", {}).get("docs", [])
                    optimized_items = []
                    for item in items:
                        optimized_items.append(
                            {
                                "title": item["headline"].get("main"),
                                "link": item["web_url"],
                                "description": item["abstract"],
                            }
                        )
                    return PluginOutput(data={"results": json.dumps(optimized_items)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
