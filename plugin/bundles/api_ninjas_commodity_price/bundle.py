from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class ApiNinjasCommodityPrice(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        city: str = "New York"
        api_ninjas_api_key: str = credentials.credentials.get("API_NINJAS_API_KEY")

        url = f"https://api.api-ninjas.com/v1/worldtime?city={city}"

        headers = {
            "X-Api-Key": api_ninjas_api_key
        }

        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()

