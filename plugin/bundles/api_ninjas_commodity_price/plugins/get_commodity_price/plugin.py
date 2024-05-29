import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GetCommodityPrice(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        name: str = plugin_input.input_params.get("name")
        api_ninjas_api_key: str = credentials.credentials.get("API_NINJAS_API_KEY")
        name = name.title()

        url = f"https://api.api-ninjas.com/v1/commodityprice?name={name}"

        headers = {"X-Api-Key": api_ninjas_api_key}

        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"result": json.dumps(data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
