import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GoogleSearchScrape(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        type: str = plugin_input.input_params.get("type", "web")
        device: str = plugin_input.input_params.get("device", None)
        gl: str = plugin_input.input_params.get("gl", None)
        google_domain: str = plugin_input.input_params.get("google_domain", None)
        location: str = plugin_input.input_params.get("location", None)
        hl: str = plugin_input.input_params.get("hl", None)
        num: int = plugin_input.input_params.get("num", None)
        page: int = plugin_input.input_params.get("page", None)

        aves_api_api_key: str = credentials.credentials.get("AVES_API_API_KEY")

        url = f"https://api.avesapi.com/search?apikey={aves_api_api_key}&type={type}&query={query}"

        if device:
            url += f"&device={device}"
        if gl:
            url += f"&gl={gl}"
        if google_domain:
            url += f"&google_domain={google_domain}"
        if location:
            url += f"&location={location}"
        if hl:
            url += f"&hl={hl}"
        if num:
            url += f"&num={num}"
        if page:
            url += f"&page={page}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("result", {})
                    return PluginOutput(data={"results": json.dumps(results)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
