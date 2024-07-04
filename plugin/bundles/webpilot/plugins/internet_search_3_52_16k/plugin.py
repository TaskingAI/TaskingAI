import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class InternetSearch35216K(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        content: str = plugin_input.input_params.get("content")
        url: str = plugin_input.input_params.get("url", None)
        webpilot_api_key: str = credentials.credentials.get("WEBPILOT_API_KEY")

        api_url = f"https://beta.webpilotai.com/api/v1/watt"

        headers = {"Authorization": f"Bearer {webpilot_api_key}", "Content-Type": "application/json"}

        if url:
            contents = " ".join([content, url])
        body = {"model": "wp-watt-3.52-16k", "content": contents}

        async with ClientSession() as session:
            async with session.post(url=api_url, headers=headers, json=body, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    results = await response.json()
                    return PluginOutput(data={"results": results.get("content", "")})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
