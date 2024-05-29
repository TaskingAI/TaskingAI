from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class GoogleSearch(BundleHandler):
    async def verify(self, credentials: BundleCredentials):

        query: str = "today's google doodle"
        api_key: str = credentials.credentials.get("GOOGLE_CUSTOM_SEARCH_API_KEY")
        engine_id: str = credentials.credentials.get("GOOGLE_CUSTOM_SEARCH_ENGINE_ID")

        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={engine_id}&q={query}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                   pass
                else:
                   raise_credentials_validation_error()
