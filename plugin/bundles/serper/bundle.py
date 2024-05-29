import json

from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Serper(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        query: str = "TaskingAI"
        SERPER_API_KEY: str = credentials.credentials.get("SERPER_API_KEY")

        url = "https://google.serper.dev/search"

        headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}

        payload = json.dumps({"q": query, "num": 20})

        async with ClientSession() as session:
            async with session.post(url, headers=headers, data=payload, proxy=CONFIG.PROXY) as response:
                if response.status != 200:
                    raise_credentials_validation_error(await response.text())
