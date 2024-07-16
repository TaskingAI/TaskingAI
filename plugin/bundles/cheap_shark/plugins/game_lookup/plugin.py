import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GameLookup(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        title: str = plugin_input.input_params.get("title")
        steam_id: int = plugin_input.input_params.get("steamAppID", None)
        limit: int = plugin_input.input_params.get("limit", None)
        exact: int = plugin_input.input_params.get("exact", None)

        api_url = f"https://www.cheapshark.com/api/1.0/games?title={title}"

        if steam_id:
            api_url += f"&steamAppID={steam_id}"

        if limit:
            api_url += f"&limit={limit}"

        if exact:
            api_url += f"&exact={exact}"

        async with ClientSession() as session:
            async with session.get(url=api_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"results": json.dumps(data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
