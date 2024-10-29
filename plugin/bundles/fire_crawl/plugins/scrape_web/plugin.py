import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class ScrapeWeb(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        url: str = plugin_input.input_params.get("url")
        only_main_content: bool = plugin_input.input_params.get("only_main_content", True)
        screenshot: bool = plugin_input.input_params.get("screenshot", False)

        fire_crawl_api_key: str = credentials.credentials.get("FIRE_CRAWL_API_KEY")

        api_url = f"https://api.firecrawl.dev/v1/scrape"

        headers = {"Authorization": f"Bearer {fire_crawl_api_key}", "Content-Type": "application/json"}

        payload = {
            "url": url,
            "onlyMainContent": only_main_content,
            "formats": [
                "markdown",
            ],
        }

        if screenshot:
            payload.get("formats").append("screenshot@fullPage")

        async with ClientSession() as session:
            async with session.post(url=api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("data", "")
                    return PluginOutput(data={"results": json.dumps(results)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
