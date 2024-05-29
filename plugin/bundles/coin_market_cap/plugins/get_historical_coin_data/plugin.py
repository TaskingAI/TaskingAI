import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GetHistoricalCoinData(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        symbol: str = plugin_input.input_params.get("symbol")
        time_start: str = plugin_input.input_params.get("time_start")
        time_end: str = plugin_input.input_params.get("time_end")
        interval: str = plugin_input.input_params.get("interval", "daily")

        coin_market_cap_api_key: str = credentials.credentials.get("COIN_MARKET_CAP_API_KEY")

        url = (
            f"https://pro-api.coinmarketcap.com/v3/cryptocurrency/quotes/historical?symbol={symbol}&interval={interval}"
        )

        if time_start:
            url += f"&time_start={time_start}"
        if time_end:
            url += f"&time_end={time_end}"

        headers = {"X-CMC_PRO_API_KEY": coin_market_cap_api_key}

        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    result = data["data"][symbol][0]["quotes"]
                    refined_results = []
                    for item in result:
                        refined_results.append(
                            {"timestamp": item["timestamp"], "price_usd": item["quote"]["USD"]["price"]}
                        )
                    return PluginOutput(data={"result": json.dumps(refined_results)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
