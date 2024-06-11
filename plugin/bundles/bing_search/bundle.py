from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class BingSearch(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        bing_search_api_key: str = credentials.credentials.get("BING_SEARCH_API_KEY")
        query = "the highest mountain in the world"
        url = f"https://api.bing.microsoft.com/v7.0/search?q={query}"

        headers = {"Ocp-Apim-Subscription-Key": bing_search_api_key}

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY, headers=headers) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
