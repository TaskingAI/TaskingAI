import json

from aiohttp import ClientSession

from app.error.error_code import raise_provider_api_error
from bundle_dependency import *


class GetHistoricalStockData(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        symbol: str = plugin_input.input_params.get("symbol")
        interval: str = plugin_input.input_params.get("interval")
        start_date: str = plugin_input.input_params.get("start_date")
        end_date: str = plugin_input.input_params.get("end_date")

        alpha_vantage_api_key: str = credentials.credentials.get("ALPHA_VANTAGE_API_KEY")

        function = ""
        result_key = ""

        if interval.lower() == 'daily':
            function = "TIME_SERIES_DAILY"
            result_key = "Time Series (Daily)"
        elif interval.lower() == 'weekly':
            function = "TIME_SERIES_WEEKLY_ADJUSTED"
            result_key = "Weekly Adjusted Time Series"
        elif interval.lower() == 'monthly':
            function = "TIME_SERIES_MONTHLY_ADJUSTED"
            result_key = "Monthly Adjusted Time Series"
        else:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid interval")

        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={alpha_vantage_api_key}'

        if interval.lower() == 'daily':
            url += f'&outputsize=full'

        async with ClientSession() as session:
            async with session.get(url=url) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data[result_key]

                    refined_results = []
                    for date, values in results.items():
                        if start_date and date < start_date:
                            continue
                        if end_date and date > end_date:
                            continue

                        refined_results.append({
                            "date": date,
                            "open": values['1. open'],
                            "high": values['2. high'],
                            "low": values['3. low'],
                            "close": values['5. adjusted close'] if interval.lower() != 'daily' else values['4. close'],
                            "volume": values['6. volume'] if interval.lower() != 'daily' else values['5. volume'],
                        })

                    return PluginOutput(data={
                        "result": json.dumps(refined_results)
                    })
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
