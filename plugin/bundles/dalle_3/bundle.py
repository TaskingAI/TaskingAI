from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Dalle3(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        openai_api_key: str = credentials.credentials.get("OPENAI_API_KEY")

        url = "https://api.openai.com/v1/models"
        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        }

        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
