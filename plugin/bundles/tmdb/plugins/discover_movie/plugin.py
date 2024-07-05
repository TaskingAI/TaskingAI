import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class DiscoverMovie(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        language: str = plugin_input.input_params.get("language", "en-US")
        page: int = plugin_input.input_params.get("page", 1)
        primary_release_year: int = plugin_input.input_params.get("primary_release_year", None)
        sort_by: str = plugin_input.input_params.get("sort_by", "popularity.desc")
        with_origin_country: str = plugin_input.input_params.get("with_origin_country", None)
        with_original_language: str = plugin_input.input_params.get("with_original_language", None)

        tmdb_api_key = credentials.credentials["TMDB_API_KEY"]

        base_url = f"https://api.themoviedb.org/3/discover/movie?api_key={tmdb_api_key}&include_adult=false&language={language}&page={page}&sort_by={sort_by}"
        if primary_release_year:
            base_url += f"&primary_release_year={primary_release_year}"
        if with_origin_country:
            base_url += f"&with_origin_country={with_origin_country.upper()}"
        if with_original_language:
            base_url += f"&with_original_language={with_original_language.lower()}"

        async with ClientSession() as session:
            async with session.get(url=base_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"results": json.dumps(data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
