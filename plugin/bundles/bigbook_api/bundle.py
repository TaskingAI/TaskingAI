from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class BigbookApi(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        api_key: str = credentials.credentials.get("BIGBOOK_API_API_KEY")
        id: str = "16384516"
        number: int = 1

        api_url = f"https://api.bigbookapi.com/{id}/similar?api-key={api_key}&number={number}"

        async with ClientSession() as session:
            async with session.get(url=api_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
