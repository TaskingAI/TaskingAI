import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class RecipeSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        cuisine: str = plugin_input.input_params.get("cuisine")
        diet: str = plugin_input.input_params.get("diet")
        include_ingredients: str = plugin_input.input_params.get("includeIngredients")
        exclude_ingredients: str = plugin_input.input_params.get("excludeIngredients")
        number: int = plugin_input.input_params.get("number")
        max_calories: int = plugin_input.input_params.get("max_calories")
        min_calories: int = plugin_input.input_params.get("min_calories")
        max_protein: int = plugin_input.input_params.get("max_protein")
        min_protein: int = plugin_input.input_params.get("min_protein")
        spoonacular_api_key: str = credentials.credentials.get("SPOONACULAR_API_KEY")

        api_url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={spoonacular_api_key}&query={query}"

        if cuisine:
            api_url += f"&cuisine={cuisine}"

        if diet:
            api_url += f"&diet={diet}"

        if include_ingredients:
            api_url += f"&includeIngredients={include_ingredients}"

        if exclude_ingredients:
            api_url += f"&excludeIngredients={exclude_ingredients}"

        if number:
            api_url += f"&number={number}"

        if max_calories:
            api_url += f"&maxCalories={max_calories}"

        if min_calories:
            api_url += f"&minCalories={min_calories}"

        if max_protein:
            api_url += f"&maxProtein={max_protein}"

        if min_protein:
            api_url += f"&minProtein={min_protein}"

        async with ClientSession() as session:
            async with session.get(url=api_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("results", [])
                    results = []
                    for item in items:
                        result = {}
                        id = item.get("id")
                        result["id"] = id
                        result["title"] = item.get("title")
                        result["image"] = item.get("image")
                        if max_calories or min_calories or max_protein or min_protein:
                            nutrition = item.get("nutrition", {})
                            result["nutrients"] = nutrition.get("nutrients", [])
                        info_url = f"https://api.spoonacular.com/recipes/{id}/information?apiKey={spoonacular_api_key}"

                        async with session.get(url=info_url, proxy=CONFIG.PROXY) as info_response:
                            if info_response.status == 200:
                                info_data = await info_response.json()
                                result["sourceUrl"] = info_data.get("sourceUrl")
                                result["summary"] = info_data.get("summary")
                                result["instructions"] = info_data.get("instructions")
                                result["spoonacularScore"] = info_data.get("spoonacularScore")
                                result["spoonacularSourceUrl"] = info_data.get("spoonacularSourceUrl")
                            else:
                                data = await info_response.json()
                                raise_provider_api_error(json.dumps(data))
                        results.append(result)
                    return PluginOutput(data={"results": json.dumps(results)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
