from aiohttp import ClientSession

from bundle_dependency import *
from app.service.image_load import get_image_base64_string
from config import CONFIG


class GeospyApi(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        GEOSPY_API_API_KEY: str = credentials.credentials.get("GEOSPY_API_API_KEY")

        image = "https://www.grandplazapenthouse.com/wp-content/uploads/sites/6/2020/03/chicago-bean.jpg"

        base64_string = await get_image_base64_string(image)

        url = f"https://dev.geospy.ai/predict"

        headers = {
            "Authorization": f"Bearer {GEOSPY_API_API_KEY}",
            "Content-Type": "application/json",
        }

        data = {"image": base64_string}

        async with ClientSession() as session:
            async with session.post(url=url, headers=headers, json=data, proxy=CONFIG.PROXY) as response:
                if response.status != 200:
                    pass
                else:
                    raise_credentials_validation_error()
