import json

from aiohttp import ClientSession


from bundle_dependency import *


class GetHourlyForecast(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        lat: float = plugin_input.input_params.get("lat", 0)
        lon: float = plugin_input.input_params.get("lon", 0)
        hours: int = plugin_input.input_params.get("hours", 24)

        base_url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "exclude": "minutely,daily,current,alerts",
            "appid": credentials.credentials.get("OPEN_WEATHER_API_KEY", ""),
            "units": "metric",
        }
        async with ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    hourly_forecast = data.get("hourly", [])
                    hourly_forecasts_selected = []
                    for forecast in hourly_forecast:
                        hourly_forecasts_selected.append(
                            {
                                "timestamp": forecast.get("dt", None),
                                "temperature_celsius": forecast.get("temp", None),
                                "pressure_hPa": forecast.get("pressure", None),
                                "humidity_%": forecast.get("humidity", None),
                                "visibility_m": forecast.get("visibility", None),
                                "weather_condition": forecast.get("weather", [{}])[0].get("main", None),
                                "rain_probability": forecast.get("pop", None),
                                "uvi": forecast.get("uvi", None),
                            }
                        )

                    return PluginOutput(data={"result": str(hourly_forecasts_selected[:hours])})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
