from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class GeminiVisionModels(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        GOOGLE_GEMINI_API_KEY: str = credentials.credentials.get("GOOGLE_GEMINI_API_KEY")

        url = f"https://generativelanguage.googleapis.com/v1beta/models"

        headers = {
            "x-goog-api-key": f" {GOOGLE_GEMINI_API_KEY}",
            "Content-Type": "application/json",
        }

        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
