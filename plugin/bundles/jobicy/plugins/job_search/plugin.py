import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class JobSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        count: int = plugin_input.input_params.get("count", 50)
        geo: str = plugin_input.input_params.get("geo")
        industry: str = plugin_input.input_params.get("industry")
        tag: str = plugin_input.input_params.get("tag")

        if count > 50 or count < 1:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR,
                message=f"Invalid count '{count}'. Supported values are between 1 and 50.",
            )

        api_url = f"https://jobicy.com/api/v2/remote-jobs?count={count}"

        if geo:
            api_url += f"&geo={geo}"

        if industry:
            api_url += f"&industry={industry}"

        if tag:
            api_url += f"&tag={tag}"

        async with ClientSession() as session:
            async with session.get(url=api_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("jobs", [])
                    return PluginOutput(data={"results": json.dumps(results)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
