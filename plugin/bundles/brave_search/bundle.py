from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class BraveSearch(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        brave_api_key: str = credentials.credentials.get("BRAVE_API_KEY")
        query: str = "Python"
        count: int = 1

        headers = {"Accept": "application/json", "Accept-Encoding": "gzip", "X-Subscription-Token": brave_api_key}

        api_url = f"https://api.search.brave.com/res/v1/web/search?q={query}&count={count}"

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
