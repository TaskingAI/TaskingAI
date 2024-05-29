import json

from aiohttp import ClientSession


from bundle_dependency import *


class ListExchangeRates(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        base_currency: str = plugin_input.input_params.get("base_currency")
        exchangerate_api_key: str = credentials.credentials.get("EXCHANGERATE_API_API_KEY")

        base_url = f"https://v6.exchangerate-api.com/v6/{exchangerate_api_key}/latest/{base_currency}"

        async with ClientSession() as session:
            async with session.get(base_url) as response:
                if response.status == 200:
                    data = await response.json()
                    rates = data["conversion_rates"]
                    return PluginOutput(data={"rates": json.dumps(rates)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
