from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class GetimgAi(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        getimg_api_key: str = credentials.credentials.get("GETIMG_API_KEY")

        api_url = "https://api.getimg.ai/v1/models"

        headers = {"accept": "application/json", "Authorization": f"Bearer {getimg_api_key}"}

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
