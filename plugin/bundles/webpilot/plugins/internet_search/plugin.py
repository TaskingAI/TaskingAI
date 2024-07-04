import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class InternetSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        content: str = plugin_input.input_params.get("content")
        model: str = plugin_input.input_params.get("model", None)
        webpilot_api_key: str = credentials.credentials.get("WEBPILOT_API_KEY")

        url = f"https://beta.webpilotai.com/api/v1/watt"

        headers = {"Authorization": f"Bearer {webpilot_api_key}", "Content-Type": "application/json"}
        if model:
            body = {"model": model, "content": content}
            async with ClientSession() as session:
                async with session.post(url=url, headers=headers, json=body, proxy=CONFIG.PROXY) as response:
                    if response.status == 200:
                        results = await response.json()
                        return PluginOutput(data={"results": results.get("content", "")})
                    else:
                        data = await response.json()
                        raise_provider_api_error(json.dumps(data))
        else:
            body_1 = {"model": "wp-watt-3.52-16k", "content": content}

            body_2 = {"model": "wp-watt-4.02-16k", "content": content}

            error_details = []

            async with ClientSession() as session:
                async with session.post(url=url, headers=headers, json=body_1, proxy=CONFIG.PROXY) as response_1:
                    if response_1.status == 200:
                        results = await response_1.json()
                        return PluginOutput(data={"results": results.get("content", "")})
                    else:
                        data_1 = await response_1.json()
                        error_details.append({"model": "wp-watt-3.52-16k", "error": data_1})

                async with session.post(url=url, headers=headers, json=body_2, proxy=CONFIG.PROXY) as response_2:
                    if response_2.status == 200:
                        results = await response_2.json()
                        return PluginOutput(data={"results": results.get("content", "")})
                    else:
                        data_2 = await response_2.json()
                        error_details.append({"model": "wp-watt-4.02-16k", "error": data_2})

            raise_provider_api_error(json.dumps(error_details))
