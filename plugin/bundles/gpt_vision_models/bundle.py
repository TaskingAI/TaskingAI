from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class GptVisionModels(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        OPENAI_API_KEY: str = credentials.credentials.get("OPENAI_API_KEY")

        url = "https://api.openai.com/v1/models"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}

        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
