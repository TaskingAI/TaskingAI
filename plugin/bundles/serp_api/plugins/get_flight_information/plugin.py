import json

from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class GetFlightInformation(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        SERP_API_API_KEY: str = credentials.credentials.get("SERP_API_API_KEY")
        departure_id: str = plugin_input.input_params.get("departure_id")
        arrival_id: str = plugin_input.input_params.get("arrival_id")
        outbound_date: str = plugin_input.input_params.get("outbound_date")
        type: int = plugin_input.input_params.get("type", 2)
        return_date: str = plugin_input.input_params.get("return_date")
        max_duration: str = plugin_input.input_params.get("max_duration")
        max_price: str = plugin_input.input_params.get("max_price")

        base_url = f"https://serpapi.com/search?engine=google_flights&departure_id={departure_id}&arrival_id={arrival_id}&outbound_date={outbound_date}&api_key={SERP_API_API_KEY}&type={type}"
        if max_duration:
            base_url += f"&max_duration={max_duration}"
        if max_price:
            base_url += f"&max_price={max_price}"
        if type == 1 and return_date:
            base_url += f"&return_date={return_date}"
        async with ClientSession() as session:
            async with session.get(base_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    best_flights = data.get("best_flights", [])
                    best_flight_info = []

                    for best_flight in best_flights:
                        best_flight_info.append(
                            {
                                "flights": best_flight.get("flights", ""),
                            }
                        )
                        flights = data.get("flights", [])
                        flight_info = []
                        for flight in flights:
                            flight_info.append(
                                {
                                    "departure_airport": flight.get("departure_airport", ""),
                                    "arrival_airport": flight.get("arrival_airport", ""),
                                    "duration": flight.get("duration", ""),
                                    "airplane": flight.get("airplane", ""),
                                    "airline": flight.get("airline", ""),
                                    "airline_logo": flight.get("airline_logo", ""),
                                    "flight_number": flight.get("flight_number", ""),
                                    "legroom": flight.get("legroom", ""),
                                }
                            )
                    return PluginOutput(data={"result": json.dumps(best_flight_info)})

                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
