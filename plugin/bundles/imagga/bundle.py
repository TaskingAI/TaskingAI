import base64
from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Imagga(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        imagga_api_key: str = credentials.credentials.get("IMAGGA_API_KEY")
        imagga_api_secret: str = credentials.credentials.get("IMAGGA_API_SECRET")

        key = f"{imagga_api_key}:{imagga_api_secret}"

        encoded_key = base64.b64encode(key.encode()).decode()

        api_url = f"https://api.imagga.com/v2/tags?image_url=https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg&limit=1"

        headers = {"Authorization": f"Basic {encoded_key}"}

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
