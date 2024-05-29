import json

import aiohttp


from bundle_dependency import *
from config import CONFIG


class Query(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        wolfram_alpha_app_id: str = credentials.credentials.get("WOLFRAM_ALPHA_APP_ID")

        url = f"https://www.wolframalpha.com/api/v1/llm-api?input={query}&appid={wolfram_alpha_app_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.text()
                    return PluginOutput(data={"result": data})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
