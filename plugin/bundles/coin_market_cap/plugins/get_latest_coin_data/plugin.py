import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GetLatestCoinData(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        symbol: str = plugin_input.input_params.get("symbol")
        coin_market_cap_api_key: str = credentials.credentials.get("COIN_MARKET_CAP_API_KEY")

        url = f"https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?symbol={symbol}"

        headers = {"X-CMC_PRO_API_KEY": coin_market_cap_api_key}

        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    currency_data = data["data"][symbol][0]
                    result_dict = {
                        "name": currency_data["name"],
                        "symbol": currency_data["symbol"],
                        "price_usd": currency_data["quote"]["USD"]["price"],
                        "percent_change_1h": currency_data["quote"]["USD"]["percent_change_1h"],
                        "percent_change_24h": currency_data["quote"]["USD"]["percent_change_24h"],
                        "percent_change_7d": currency_data["quote"]["USD"]["percent_change_7d"],
                        "market_cap_usd": currency_data["quote"]["USD"]["market_cap"],
                        "last_updated": currency_data["quote"]["USD"]["last_updated"],
                    }
                    return PluginOutput(data={"result": json.dumps(result_dict)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
