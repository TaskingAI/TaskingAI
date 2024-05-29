from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class CalorieNinjas(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        food_description: str = '10oz onion and a tomato'
        calorie_ninjas_api_key: str = credentials.credentials.get("CALORIE_NINJAS_API_KEY")

        url = f"https://api.calorieninjas.com/v1/nutrition?query={food_description}"

        headers = {
            "X-Api-Key": calorie_ninjas_api_key
        }

        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()