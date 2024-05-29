from aiohttp import ClientSession

from bundle_dependency import *


class ExchangerateApi(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        from_currency: str = "USD"
        to_currency: str = "EUR"
        exchangerate_api_key: str = credentials.credentials.get("EXCHANGERATE_API_API_KEY")

        base_url = f"https://v6.exchangerate-api.com/v6/{exchangerate_api_key}/pair/{from_currency}/{to_currency}"

        async with ClientSession() as session:
            async with session.get(base_url) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()

