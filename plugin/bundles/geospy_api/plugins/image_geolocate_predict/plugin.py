import json

from aiohttp import ClientSession

from app.service.image_load import get_image_base64_string
from bundle_dependency import *
from config import CONFIG


class ImageGeolocatePredict(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        image: str = plugin_input.input_params.get("image")
        top_k: int = plugin_input.input_params.get("top_k")
        GEOSPY_API_API_KEY: str = credentials.credentials.get("GEOSPY_API_API_KEY")

        url = f"https://dev.geospy.ai/predict"

        headers = {
            "Authorization": f"Bearer {GEOSPY_API_API_KEY}",
            "Content-Type": "application/json",
        }

        base64_string = await get_image_base64_string(image)

        data = {
            "image": base64_string,
        }
        if top_k:
            data["top_k"] = top_k

        async with ClientSession() as session:
            async with session.post(url=url, headers=headers, json=data, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    geo_predictions = data.get("geo_predictions", "")
                    results = []
                    for geo_prediction in geo_predictions:
                        results.append(
                            {
                                "coordinates": geo_prediction["coordinates"],
                                "address": geo_prediction["address"],
                            }
                        )
                    return PluginOutput(data={"results": json.dumps(results)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
