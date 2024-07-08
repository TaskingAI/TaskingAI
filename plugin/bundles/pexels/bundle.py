from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Pexels(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        api_key: str = credentials.credentials.get("PEXELS_API_KEY")
        query: str = "nature"

        api_url = f"https://api.pexels.com/v1/search?query={query}"
        headers = {"Authorization": api_key}

        async with ClientSession() as session:
            async with session.get(api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
