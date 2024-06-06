import json

from aiohttp import ClientSession


from bundle_dependency import *


class GetCommodityPriceLatest(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        symbols: str = plugin_input.input_params.get("symbols")
        base: str = plugin_input.input_params.get("base")
        edit_symbols = ",".join(part.strip() for part in symbols.split(","))
        access_key: str = credentials.credentials.get("COMMODITIES_API_API_KEY", "")

        url = f"https://commodities-api.com/api/latest?access_key={access_key}&symbols={edit_symbols}"

        if base:
            if len(base) != 3:
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message=f"Invalid base {base}. Supported base is the three-letter currency code or commodity code of your preferred base currency.",
                )
            base = base.upper()
            url += f"&base={base}"

        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    data = data.get("data", {})
                    date: str = data.get("date", None)
                    base: str = data.get("base", None)

                    rates: float = data.get("rates", None)
                    keys = [key.upper() for key in edit_symbols.split(",")]
                    inverted_rates = {key: 1 / rates[key] for key in keys if key in rates}

                    unit: str = data.get("unit", None)
                    timestamp: int = data.get("timestamp", None)
                    return PluginOutput(
                        data={
                            "result": json.dumps(
                                {
                                    "base": base,
                                    "rates": inverted_rates,
                                    "unit": unit,
                                    "date": date,
                                    "timestamp": timestamp,
                                }
                            )
                        }
                    )
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
