import json

from aiohttp import ClientSession


from bundle_dependency import *


class GetDailyForecast(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        lat: float = plugin_input.input_params.get("lat", 0)
        lon: float = plugin_input.input_params.get("lon", 0)
        days: int = plugin_input.input_params.get("days", 7)

        base_url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "exclude": "minutely,hourly,current,alerts",
            "appid": credentials.credentials.get("OPEN_WEATHER_API_KEY", ""),
            "units": "metric",
        }
        async with ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    daily_forecast = data.get("daily", [])
                    daily_forecasts_selected = []
                    for forecast in daily_forecast:
                        daily_forecasts_selected.append(
                            {
                                "timestamp": forecast.get("dt", None),
                                "summary": forecast.get("summary", None),
                                "temperature_max_celsius": forecast.get("temp", {}).get("max", None),
                                "temperature_min_celsius": forecast.get("temp", {}).get("min", None),
                                "pressure_hPa": forecast.get("pressure", None),
                                "humidity_%": forecast.get("humidity", None),
                                "weather_condition": forecast.get("weather", [{}])[0].get("main", None),
                                "cloudiness": forecast.get("clouds", None),
                                "rain_probability": forecast.get("pop", None),
                                "uvi": forecast.get("uvi", None),
                            }
                        )

                    return PluginOutput(data={"result": str(daily_forecasts_selected[:days])})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
