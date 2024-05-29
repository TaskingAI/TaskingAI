import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GetTimeByTimezone(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        timezone: str = plugin_input.input_params.get("timezone")
        url = f"https://timeapi.io/api/Time/current/zone?timeZone={timezone}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    result = await response.json()
                    return PluginOutput(data={"result": json.dumps(result)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
