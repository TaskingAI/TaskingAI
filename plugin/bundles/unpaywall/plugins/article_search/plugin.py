import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class ArticleSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        email: str = plugin_input.input_params.get("email")
        is_oa: bool = plugin_input.input_params.get("is_oa", None)
        page: int = plugin_input.input_params.get("page", None)

        api_url = f"https://api.unpaywall.org/v2/search?query={query}&email={email}"

        if is_oa:
            api_url += f"&is_oa={is_oa}"

        if page:
            api_url += f"&page={page}"

        async with ClientSession() as session:
            async with session.get(url=api_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"results": json.dumps(data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
