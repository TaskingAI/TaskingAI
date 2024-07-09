from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Spoonacular(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        spoonacular_api_key: str = credentials.credentials.get("SPOONACULAR_API_KEY")

        query: str = "pasta"
        number: int = 2
        max_calories: int = 1000

        url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={spoonacular_api_key}&query={query}&number={number}&maxCalories={max_calories}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
