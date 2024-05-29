import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GetNutritionInfo(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        food_description: str = plugin_input.input_params.get("food_description")
        calorie_ninjas_api_key: str = credentials.credentials.get("CALORIE_NINJAS_API_KEY")

        url = f"https://api.calorieninjas.com/v1/nutrition?query={food_description}"

        headers = {"X-Api-Key": calorie_ninjas_api_key}

        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"result": json.dumps(data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
