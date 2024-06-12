from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Perplexity(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        content: str = "Hello!"
        PERPLEXITY_API_KEY: str = credentials.credentials.get("PERPLEXITY_API_KEY")

        url = f"https://api.perplexity.ai/chat/completions"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        }

        data = {"model": "llama-3-sonar-small-32k-online", "messages": [{"role": "user", "content": f"{content}"}]}

        async with ClientSession() as session:
            async with session.post(url=url, hearders=headers, proxy=CONFIG.PROXY, json=data) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
