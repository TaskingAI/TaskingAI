from typing import List
import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class WebpageRetrieve(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        cmd: str = plugin_input.input_params.get("cmd")
        url: str = plugin_input.input_params.get("url", None)
        fields: List[str] = plugin_input.input_params.get("fields", None)
        multion_api_key: str = credentials.credentials.get("MULTION_API_KEY")

        if url and fields:
            api_url = f"https://api.multion.ai/v1/web/retrieve"
            data = {"cmd": cmd, "url": url, "fields": fields}
        else:
            api_url = f"https://api.multion.ai/v1/web/browse"
            data = {"cmd": cmd}
            if url:
                data["url"] = url

        headers = {
            "X_MULTION_API_KEY": multion_api_key,
            "Content-Type": "application/json",
        }

        async with ClientSession() as session:
            async with session.post(url=api_url, headers=headers, json=data, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    results = json.dumps(data)
                    return PluginOutput(data={"results": results})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
