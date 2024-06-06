import json

from aiohttp import ClientSession

from bundle_dependency import *


class GetCommodityPriceTimeSeries(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        start_date: str = plugin_input.input_params.get("start_date")
        end_date: str = plugin_input.input_params.get("end_date")
        symbols: str = plugin_input.input_params.get("symbols")
        access_key: str = credentials.credentials.get("COMMODITIES_API_API_KEY", "")

        url = f"https://commodities-api.com/api/timeseries?access_key={access_key}&start_date={start_date}&end_date={end_date}&symbols={symbols}"

        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    data = data.get("data", {})
                    date: str = data.get("date", None)
                    base: str = data.get("base", None)
                    rates: float = data.get("rates", None)
                    unit: str = data.get("unit", None)
                    start_date: str = data.get("start_date", None)
                    end_date: str = data.get("end_date", None)
                    return PluginOutput(
                        data={
                            "result": json.dumps(
                                {
                                    "base": base,
                                    "rates": rates,
                                    "unit": unit,
                                    "date": date,
                                    "start_date": start_date,
                                    "end_date": end_date,
                                }
                            )
                        }
                    )
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
