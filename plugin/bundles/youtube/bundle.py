import aiohttp

from bundle_dependency import *
from config import CONFIG


class Youtube(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        query: str = 'taskingai'
        GOOGLE_API_KEY: str = credentials.credentials.get("GOOGLE_API_KEY")

        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&key={GOOGLE_API_KEY}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
