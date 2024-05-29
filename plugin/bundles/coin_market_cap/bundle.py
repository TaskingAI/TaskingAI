from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class CoinMarketCap(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        symbol: str = "ETH"
        coin_market_cap_api_key: str = credentials.credentials.get("COIN_MARKET_CAP_API_KEY")

        url = f"https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?symbol={symbol}"

        headers = {
            "X-CMC_PRO_API_KEY": coin_market_cap_api_key
        }

        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()

