import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GameInfo(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        ids: str = plugin_input.input_params.get("ids")

        api_url = f"https://www.cheapshark.com/api/1.0/games?ids={ids}"

        async with ClientSession() as session:
            async with session.get(url=api_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"results": json.dumps(data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
