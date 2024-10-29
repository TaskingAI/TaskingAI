import json

from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class GetAnswerFromPerplexity(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        content: str = plugin_input.input_params.get("content")
        model: str = plugin_input.input_params.get("model", "llama-3.1-sonar-small-128k-online")
        perplexity_api_key: str = credentials.credentials.get("PERPLEXITY_API_KEY")

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {perplexity_api_key}",
        }

        data = {"model": model, "messages": [{"role": "user", "content": content}]}

        url = f"https://api.perplexity.ai/chat/completions"

        async with ClientSession() as session:
            async with session.post(url=url, headers=headers, proxy=CONFIG.PROXY, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    results = response_data.get("choices", [])[0]["message"]["content"]
                    return PluginOutput(data={"results": results})
                else:
                    response_json = await response.json()
                    raise_provider_api_error(json.dumps(response_json))
