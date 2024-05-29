from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class AlphaVantage(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        symbol: str = "NVDA"

        alpha_vantage_api_key: str = credentials.credentials.get("ALPHA_VANTAGE_API_KEY")

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={alpha_vantage_api_key}'

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()


