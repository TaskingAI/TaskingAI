from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Nytimes(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        NEW_YORK_TIMES_API_KEY: str = credentials.credentials.get("NEW_YORK_TIMES_API_KEY")

        query = "Trump"
        url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={NEW_YORK_TIMES_API_KEY}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
