import json

from aiohttp import ClientSession


from bundle_dependency import *


class GetExchangeRate(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        from_currency: str = plugin_input.input_params.get("from_currency")
        to_currency: str = plugin_input.input_params.get("to_currency")
        exchangerate_api_key: str = credentials.credentials.get("EXCHANGERATE_API_API_KEY")

        base_url = f"https://v6.exchangerate-api.com/v6/{exchangerate_api_key}/pair/{from_currency}/{to_currency}"

        async with ClientSession() as session:
            async with session.get(base_url) as response:
                if response.status == 200:
                    data = await response.json()
                    rate: float = data["conversion_rate"]
                    return PluginOutput(data={"rate": rate})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
