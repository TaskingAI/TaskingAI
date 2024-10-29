from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Serply(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        serply_api_key: str = credentials.credentials.get("SERPLY_API_KEY")

        api_url = "https://api.serply.io/v1/search/q=trump"

        headers = {"Content-Type": "application/json", "X-Api-Key": serply_api_key}

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
