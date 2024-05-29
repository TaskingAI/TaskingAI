from bundle_dependency import *
import aiohttp
from bs4 import BeautifulSoup

from config import CONFIG


class ReadWebPage(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        url: str = plugin_input.input_params.get("url")

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status != 200:
                    raise_http_error(
                        ErrorCode.UNKNOWN_ERROR,
                        "Failed to read the web page, please make sure the page is publicly accessible.",
                    )

                data = await response.text()
                soup = BeautifulSoup(data, "html.parser")
                text = soup.get_text(separator=" ", strip=True)

                return PluginOutput(data={"result": text})
