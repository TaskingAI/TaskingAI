import aiohttp

from bundle_dependency import *
from config import CONFIG


class WolframAlpha(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        query: str = "the top 5 highest mountain in the world"
        wolfram_alpha_app_id: str = credentials.credentials.get("WOLFRAM_ALPHA_APP_ID")

        url = f"https://www.wolframalpha.com/api/v1/llm-api?input={query}&appid={wolfram_alpha_app_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()