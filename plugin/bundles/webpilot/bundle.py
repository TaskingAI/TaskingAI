from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Webpilot(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        api_key: str = credentials.credentials.get("WEBPILOT_API_KEY")
        content: str = "Who is the founder of Nintendo?"
        url: str = " https://en.wikipedia.org/wiki/Nintendo"

        api_url = f"https://beta.webpilotai.com/api/v1/watt"

        contents = " ".join([content, url])

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        body = {"model": "wp-watt-3.52-16k", "content": contents}

        async with ClientSession() as session:
            async with session.post(url=api_url, headers=headers, json=body, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    return True

        raise_credentials_validation_error()
