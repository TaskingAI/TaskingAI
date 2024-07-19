from bundle_dependency import *

from config import CONFIG

from aiohttp import ClientSession


class Multion(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        MULTION_API_KEY: str = credentials.credentials.get("MULTION_API_KEY")
        cmd: str = "Find the top post on Hackernews and get its title and points."

        api_url = f"https://api.multion.ai/v1/web/browse"

        headers = {
            "X_MULTION_API_KEY": MULTION_API_KEY,
            "Content-Type": "application/json",
        }
        data = {"cmd": cmd}
        async with ClientSession() as session:
            async with session.post(url=api_url, headers=headers, json=data, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
