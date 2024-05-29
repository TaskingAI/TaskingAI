import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class LocationDetails(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        location_id: str = plugin_input.input_params.get("location_id")
        TRIP_ADVISOR_API_KEY: str = credentials.credentials.get("TRIP_ADVISOR_API_KEY")

        url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/details?key={TRIP_ADVISOR_API_KEY}&language=en&currency=USD"
        headers = {"accept": "application/json"}

        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    information_dict = {
                        "name": data.get("name"),
                        "location_id": data.get("location_id"),
                        "address": data.get("address_obj").get("address_string"),
                        "phone": data.get("phone"),
                        "website": data.get("website"),
                        "latitude": data.get("latitude"),
                        "longitude": data.get("longitude"),
                        "rating": data.get("rating"),
                        "num_reviews": data.get("num_reviews"),
                        "ranking_data": data.get("ranking_data"),
                        "price_level": data.get("price_level"),
                        "description": data.get("description"),
                        "open_hours": data.get("open", {}).get("weekday_text", ""),
                        "features": data.get("features"),
                    }

                    return PluginOutput(status=response.status, data={"result": json.dumps(information_dict)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
