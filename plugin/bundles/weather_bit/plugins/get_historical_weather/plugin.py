import json

from aiohttp import ClientSession
from datetime import datetime


from bundle_dependency import *
from config import CONFIG


def validate_date_format(date_str):
    formats = ["%Y-%m-%d", "%Y-%m-%d:%H"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def validate_date_range(start_date, end_date):
    start_dt = validate_date_format(start_date)
    end_dt = validate_date_format(end_date)

    if not start_dt or not end_dt:
        return False, "Date format is not valid. Should be YYYY-MM-DD or YYYY-MM-DD:HH"

    if start_dt >= end_dt:
        return False, "end_date must be after start_date"

    return True, ""


class GetHistoricalWeather(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        interval: str = plugin_input.input_params.get("interval")
        start_date: str = plugin_input.input_params.get("start_date")
        end_date: str = plugin_input.input_params.get("end_date")
        lat: float = plugin_input.input_params.get("lat")
        lon: float = plugin_input.input_params.get("lon")
        units: str = plugin_input.input_params.get("units")
        tz: str = plugin_input.input_params.get("tz")
        weather_bit_api_key: str = credentials.credentials.get("WEATHER_BIT_API_KEY")
        unit_tmp = {"M": "Metric", "S": "Scientific", "I": "Fahrenheit"}

        is_valid, msg = validate_date_range(start_date, end_date)

        if not is_valid:
            raise_http_error("REQUEST_VALIDATION_ERROR", msg)

        url = f"https://api.weatherbit.io/v2.0/history/{interval}?lat={lat}&lon={lon}&start_date={start_date}&end_date={end_date}&key={weather_bit_api_key}"

        if units:
            url += f"&units={units}"
            unit = unit_tmp.get(units, "")
        else:
            unit = "Metric"
        if tz:
            url += f"&tz={tz}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    historical_weather = data.get("data", [])
                    historical_weather_selected = []

                    for history in historical_weather:
                        if interval == "daily":
                            historical_weather_selected.append(
                                {
                                    "timestamp": history.get("ts", None),
                                    "temperature_unit": unit,
                                    "temperature": history.get("temp", None),
                                    "max_temperature": history.get("max_temp", None),
                                    "min_temperature": history.get("min_temp", None),
                                    "pressure_mb": history.get("pres", None),
                                    "humidity_%": history.get("rh", None),
                                    "cloudiness": history.get("clouds", None),
                                    "max_uvi": history.get("max_uv", None),
                                }
                            )
                        else:
                            historical_weather_selected.append(
                                {
                                    "timestamp": history.get("ts", None),
                                    "temperature_unit": unit,
                                    "temperature": history.get("temp", None),
                                    "weather_condition": history.get("weather", {}).get("description", None),
                                    "pressure_mb": history.get("pres", None),
                                    "humidity_%": history.get("rh", None),
                                    "cloudiness": history.get("clouds", None),
                                    "uv_index": history.get("uv", None),
                                    "visibility_km": history.get("vis", None),
                                }
                            )
                    return PluginOutput(data={"result": json.dumps(historical_weather_selected)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
