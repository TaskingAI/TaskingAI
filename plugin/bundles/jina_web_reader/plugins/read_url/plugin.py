import aiohttp

from bundle_dependency import *


class ReadUrl(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        url: str = plugin_input.input_params.get("url")

        jina_reader_url = f"https://r.jina.ai/{url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url=jina_reader_url) as response:
                if response.status != 200:
                    raise_http_error(
                        ErrorCode.UNKNOWN_ERROR,
                        "Failed to read the web page, please make sure the page is publicly accessible.",
                    )

                data = await response.text()

                return PluginOutput(data={"result": data})
