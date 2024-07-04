from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Webpilot(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        api_key: str = credentials.credentials.get("WEBPILOT_API_KEY")
        content: str = "Who is the founder of Nintendo? https://en.wikipedia.org/wiki/Nintendo"

        url = f"https://beta.webpilotai.com/api/v1/watt"

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        body_1 = {"model": "wp-watt-3.52-16k", "content": content}

        body_2 = {"model": "wp-watt-4.02-16k", "content": content}

        async with ClientSession() as session:
            async with session.post(url=url, headers=headers, json=body_1, proxy=CONFIG.PROXY) as response_1:
                if response_1.status == 200:
                    return True

            async with session.post(url=url, headers=headers, json=body_2, proxy=CONFIG.PROXY) as response_2:
                if response_2.status == 200:
                    return True

        raise_credentials_validation_error()
