import json
import re

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


def is_valid_date(date: str):
    valid_options = {"today", "thisweek", "thismonth", "last7days", "last30days", "last3months", "yeartodate"}

    date_pattern = r"^\d{4}-\d{2}-\d{2}$"

    if date in valid_options or re.match(date_pattern, date):
        return True

    date_range_pattern = r"^\d{4}-\d{2}-\d{2},\d{4}-\d{2}-\d{2}$"
    if re.match(date_range_pattern, date):
        return True

    raise_http_error(
        ErrorCode.REQUEST_VALIDATION_ERROR,
        message=f"Invalid date '{date}'. Supported formats are: 'today', 'thisweek', 'thismonth', 'last7days', 'last30days', 'last3months', 'yeartodate', or 'YYYY-MM-DD'. For a date range, use 'YYYY-MM-DD,YYYY-MM-DD'.",
    )


class FinanceNewsSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, execution_config: Dict, plugin_input: PluginInput) -> PluginOutput:
        date: str = plugin_input.input_params.get("date", None)
        keyword: str = plugin_input.input_params.get("keyword", None)
        limit: int = plugin_input.input_params.get("limit", 25)
        source: str = plugin_input.input_params.get("source", None)
        tags: str = plugin_input.input_params.get("tags", None)
        tickers: str = plugin_input.input_params.get("tickers", None)

        finance_news_api_key: str = credentials.credentials.get("FINANCE_NEWS_API_KEY")

        if limit < 1 or limit > 100:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR, message="Invalid limit. Supported values are between 1 and 100."
            )

        api_url = f"https://api.apilayer.com/financelayer/news?limit={limit}"
        if date and is_valid_date(date):
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
