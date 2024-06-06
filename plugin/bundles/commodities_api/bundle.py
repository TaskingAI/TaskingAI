from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class CommoditiesApi(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        COMMODITIES_API_API_KEY: str = credentials.credentials.get("COMMODITIES_API_API_KEY", "")
        symbols = "RICE,WHEAT,SUGAR"
        url = f"https://commodities-api.com/api/latest?access_key={COMMODITIES_API_API_KEY}&symbols={symbols}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
