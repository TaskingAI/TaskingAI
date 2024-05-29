import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GetLatestStockData(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        symbol: str = plugin_input.input_params.get("symbol")

        alpha_vantage_api_key: str = credentials.credentials.get("ALPHA_VANTAGE_API_KEY")

        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={alpha_vantage_api_key}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data["Time Series (5min)"]
                    sorted_keys = sorted(results.keys())
                    timestamp = sorted_keys[-1]
                    price = results[timestamp]["4. close"]

                    return PluginOutput(data={"result": json.dumps({"timestamp": timestamp, "price": price})})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
