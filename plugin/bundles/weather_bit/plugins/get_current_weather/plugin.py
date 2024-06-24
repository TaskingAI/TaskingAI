import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GetCurrentWeather(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        lat: float = plugin_input.input_params.get("lat")
        lon: float = plugin_input.input_params.get("lon")
        units: str = plugin_input.input_params.get("units", "")
        weather_bit_api_key: str = credentials.credentials.get("WEATHER_BIT_API_KEY")
        unit_tmp = {"M": "Metric", "S": "Scientific", "I": "Fahrenheit"}

        url = f"https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={weather_bit_api_key}"

        if units:
            url += f"&units={units.upper()}"
            unit = unit_tmp.get(units.upper(), "")
        else:
            unit = "Metric"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data.get("data", {})[0]
                    result = {
                        "city_name": content.get("city_name", ""),
                        "country_code": content.get("country_code", ""),
                        "unit": unit,
                        "temperature": content.get("temp", ""),
                        "feels_like_temperature": content.get("app_temp", ""),
                        "weather_condition": content.get("weather", {}).get("description", ""),
                        "aqi": content.get("aqi", ""),
                        "uv_index": content.get("uv", ""),
                        "pressure": content.get("pres", ""),
                        "wind_spd": content.get("wind_spd", ""),
                        "wind_cdir": content.get("wind_cdir_full", ""),
                        "sunrise": content.get("sunrise", ""),
                        "sunset": content.get("sunset", ""),
                    }
                    return PluginOutput(data=result)
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
