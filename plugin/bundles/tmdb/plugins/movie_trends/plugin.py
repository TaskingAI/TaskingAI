import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class MovieTrends(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        time_window: str = plugin_input.input_params.get("time_window", "day")
        language: str = plugin_input.input_params.get("language", "en-US")

        tmdb_api_key = credentials.credentials.get("TMDB_API_KEY")

        base_url = f"https://api.themoviedb.org/3/trending/movie/{time_window.lower()}?api_key={tmdb_api_key}&language={language}"

        async with ClientSession() as session:
            async with session.get(url=base_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"results": json.dumps(data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
