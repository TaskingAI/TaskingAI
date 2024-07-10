from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class FinanceNews(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        api_key: str = credentials.credentials.get("FINANCE_NEWS_API_KEY")

        api_url = f"https://api.apilayer.com/financelayer/news"

        headers = {"apikey": api_key}

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
