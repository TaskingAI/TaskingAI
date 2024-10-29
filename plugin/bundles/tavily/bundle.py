from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Tavily(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        tavily_api_key: str = credentials.credentials.get("TAVILY_API_KEY")
        query: str = "Who is Trump?"

        api_url = "https://api.tavily.com/search"

        body = {"api_key": tavily_api_key, "query": query}

        headers = {"Content-Type": "application/json"}

        async with ClientSession() as session:
            async with session.post(url=api_url, json=body, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
