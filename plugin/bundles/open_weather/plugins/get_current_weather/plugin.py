import json

from aiohttp import ClientSession


from bundle_dependency import *


class GetCurrentWeather(PluginHandler):
    def celsius_to_fahrenheit(self, celsius: float) -> float:
        return (celsius * 9 / 5) + 32

    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        lat: float = plugin_input.input_params.get("lat", 0)
        lon: float = plugin_input.input_params.get("lon", 0)

        base_url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "exclude": "minutely,hourly,daily,alerts",
            "appid": credentials.credentials.get("OPEN_WEATHER_API_KEY", ""),
            "units": "metric",
        }
        async with ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    data = data.get("current", {})
                    temperature: float = data.get("temp", None)
                    feels_like: float = data.get("feels_like", None)
                    pressure: float = data.get("pressure", None)
                    humidity: float = data.get("humidity", None)
                    uvi: float = data.get("uvi", None)
                    visibility: float = data.get("visibility", None)
                    weather_condition: str = data.get("weather", [{}])[0].get("main", None)
                    timestamp: int = data.get("dt", None)
                    return PluginOutput(
                        data={
                            "temperature_celsius": temperature,
                            "temperature_fahrenheit": self.celsius_to_fahrenheit(temperature),
                            "feels_like_celsius": feels_like,
                            "feels_like_fahrenheit": self.celsius_to_fahrenheit(feels_like),
                            "pressure": pressure,
                            "humidity": humidity,
                            "uvi": uvi,
                            "visibility": visibility,
                            "weather_condition": weather_condition,
                            "timestamp": timestamp,
                        }
                    )
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
