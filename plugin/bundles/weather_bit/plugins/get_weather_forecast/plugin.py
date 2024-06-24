import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GetWeatherForecast(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        interval: str = plugin_input.input_params.get("interval")
        lat: float = plugin_input.input_params.get("lat")
        lon: float = plugin_input.input_params.get("lon")
        units: str = plugin_input.input_params.get("units")
        hours: int = plugin_input.input_params.get("hours")
        weather_bit_api_key: str = credentials.credentials.get("WEATHER_BIT_API_KEY")
        unit_tmp = {"M": "Metric", "S": "Scientific", "I": "Fahrenheit"}

        url = f"https://api.weatherbit.io/v2.0/forecast/{interval}?lat={lat}&lon={lon}&key={weather_bit_api_key}"
        if interval == "hourly" and hours:
            url += f"&hours={hours}"
        if units:
            url += f"&units={units}"
            unit = unit_tmp.get(units, "")
        else:
            unit = "Metric"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    weather_forecast = data.get("data", [])
                    weather_forecast_selected = []

                    for forecast in weather_forecast:
                        if interval == "hourly":
                            weather_forecast_selected.append(
                                {
                                    "timestamp": forecast.get("ts", None),
                                    "temperature_unit": unit,
                                    "temperature": forecast.get("temp", None),
                                    "weather_condition": forecast.get("weather", {}).get("description", None),
                                    "rain_probability": forecast.get("pop", None),
                                    "humidity_%": forecast.get("rh", None),
                                    "pressure_mb": forecast.get("pres", None),
                                    "uvi": forecast.get("uv", None),
                                    "visibility_km": forecast.get("vis", None),
                                }
                            )
                        else:
                            weather_forecast_selected.append(
                                {
                                    "timestamp": forecast.get("ts", None),
                                    "temperature_unit": unit,
                                    "temperature": forecast.get("temp", None),
                                    "max_temperature": forecast.get("max_temp", None),
                                    "min_temperature": forecast.get("min_temp", None),
                                    "pressure_mb": forecast.get("pres", None),
                                    "humidity_%": forecast.get("rh", None),
                                    "visibility_m": forecast.get("vis", None),
                                    "weather_condition": forecast.get("weather", {}).get("description", None),
                                    "rain_probability": forecast.get("pop", None),
                                    "uvi": forecast.get("uv", None),
                                }
                            )
                    return PluginOutput(data={"result": json.dumps(weather_forecast_selected)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
