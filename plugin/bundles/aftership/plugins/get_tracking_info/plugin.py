import json

from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class GetTrackingInfo(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        tracking_number: str = plugin_input.input_params.get("tracking_number")
        slug: str = plugin_input.input_params.get("slug")
        aftership_api_key: str = credentials.credentials.get("AFTERSHIP_API_KEY")

        data_first_try = await self.get_tracking(slug, tracking_number, aftership_api_key)
        if data_first_try is not None:
            return PluginOutput(data={"result": json.dumps(data_first_try)})
        else:
            data_second_try = await self.create_tracking(slug, tracking_number, aftership_api_key)
            if data_second_try:
                data = await self.get_tracking(slug, tracking_number, aftership_api_key)
                if data is not None:
                    return PluginOutput(data={"result": json.dumps(data)})
                else:
                    raise_provider_api_error(json.dumps(data))
            else:
                raise_provider_api_error(json.dumps(data_second_try))

    async def create_tracking(self, slug: str, tracking: str, api_key: str):
        url = f"https://api.aftership.com/tracking/2024-01/trackings"

        headers = {"as-api-key": api_key, "Content-Type": "application/json"}

        body = {"tracking": {"tracking_number": tracking, "slug": slug}}

        async with ClientSession() as session:
            async with session.post(url=url, headers=headers, json=body, proxy=CONFIG.PROXY) as response:
                if response.status == 201:
                    data = await response.json()
                    return True
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))

    async def get_tracking(self, slug: str, tracking: str, api_key: str):
        url = f"https://api.aftership.com/tracking/2024-01/trackings/{slug}/{tracking}"

        headers = {"as-api-key": api_key, "Content-Type": "application/json"}

        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    return None
