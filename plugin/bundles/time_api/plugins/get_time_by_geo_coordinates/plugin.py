import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GetTimeByGeoCoordinates(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        latitude: float = plugin_input.input_params.get("latitude")
        longitude: float = plugin_input.input_params.get("longitude")

        url = f"https://timeapi.io/api/Time/current/coordinate?latitude={latitude}&longitude={longitude}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    result = await response.json()
                    return PluginOutput(data={"result": json.dumps(result)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
