import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class MovieSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        language: str = plugin_input.input_params.get("language", "en-US")
        page: int = plugin_input.input_params.get("page", 1)

        tmdb_api_key = credentials.credentials["TMDB_API_KEY"]

        api_url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&language={language}&query={query}&page={page}&include_adult=False"

        async with ClientSession() as session:
            async with session.get(url=api_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"results": json.dumps(data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
