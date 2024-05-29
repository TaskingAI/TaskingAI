import json

from aiohttp import ClientSession


from bundle_dependency import *
import urllib.parse

from config import CONFIG


class SearchLocation(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        category: str = plugin_input.input_params.get("category")
        TRIP_ADVISOR_API_KEY: str = credentials.credentials.get("TRIP_ADVISOR_API_KEY")

        query = urllib.parse.quote_plus(query)
        url = (
            f"https://api.content.tripadvisor.com/api/v1/location/search?key={TRIP_ADVISOR_API_KEY}&searchQuery={query}"
        )

        if category:
            url += f"&category={category}"

        async with ClientSession() as session:
            async with session.get(url=url, headers={"accept": "application/json"}, proxy=CONFIG.PROXY) as response:

                if response.status == 200:
                    data = await response.json()
                    locations = []

                    for location in data.get("data", ()):
                        locations.append(
                            {
                                "location_id": location.get("location_id"),
                                "name": location.get("name"),
                                "address": location.get("address_obj").get("address_string"),
                            }
                        )

                    return PluginOutput(status=response.status, data={"result": json.dumps(locations)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
