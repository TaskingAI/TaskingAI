import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class ImageSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        orientation: str = plugin_input.input_params.get("orientation", None)
        size: str = plugin_input.input_params.get("size", None)
        color: str = plugin_input.input_params.get("color", None)
        locale: str = plugin_input.input_params.get("locale", None)
        page: int = plugin_input.input_params.get("page", None)
        per_page: int = plugin_input.input_params.get("per_page", None)

        pexels_api_key: str = credentials.credentials.get("PEXELS_API_KEY")

        api_url = f"https://api.pexels.com/v1/search?query={query}"
        if orientation:
            api_url += f"&orientation={orientation}"
        if size:
            api_url += f"&size={size}"
        if color:
            api_url += f"&color={color}"
        if locale:
            api_url += f"&locale={locale}"
        if page:
            api_url += f"&page={page}"
        if per_page:
            api_url += f"&per_page={per_page}"

        headers = {"Authorization": pexels_api_key}

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    results = []
                    photos = data.get("photos", [])
                    for photo in photos:
                        results.append(
                            {
                                "id": photo["id"],
                                "width": photo["width"],
                                "height": photo["height"],
                                "url": photo["url"],
                                "src": photo["src"],
                                "description": photo["alt"],
                            }
                        )
                    return PluginOutput(data={"results": json.dumps(results)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
