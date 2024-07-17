import json

from aiohttp import ClientSession


from bundle_dependency import *


class GetCommodityPriceHistorical(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        date: str = plugin_input.input_params.get("YYYY-MM-DD")
        symbols: str = plugin_input.input_params.get("symbols").upper()
        access_key: str = credentials.credentials.get("COMMODITIES_API_API_KEY", "")

        url = f"https://commodities-api.com/api/{date}?access_key={access_key}&symbols={symbols}"

        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    data = data.get("data", {})
                    date: str = data.get("date", None)
                    base: str = data.get("base", None)

                    rates: float = data.get("rates", None)
                    inverted_rates = {symbols: 1 / rates[symbols]}

                    unit: str = data.get("unit", None)
                    return PluginOutput(
                        data={
                            "result": json.dumps(
                                {
                                    "base": base,
                                    "rates": inverted_rates,
                                    "unit": unit,
                                    "date": date,
                                }
                            )
                        }
                    )
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
