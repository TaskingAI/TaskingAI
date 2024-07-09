import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class SimilarBooks(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        id: str = plugin_input.input_params.get("id")
        number: int = plugin_input.input_params.get("number", None)
        bigbook_api_key: str = credentials.credentials.get("BIGBOOK_API_API_KEY")

        api_url = f"https://api.bigbookapi.com/{id}/similar?api-key={bigbook_api_key}"

        if number:
            if number < 1 or number > 100:
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message=f"Invalid number '{number}'. The number must be between 1 and 100.",
                )
            api_url += f"&number={number}"

        async with ClientSession() as session:
            async with session.get(url=api_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"results": json.dumps(data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
