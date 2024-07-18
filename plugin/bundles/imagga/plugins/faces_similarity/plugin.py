import json
import base64

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class FacesSimilarity(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        face_id: str = plugin_input.input_params.get("face_id")
        second_face_id: str = plugin_input.input_params.get("second_face_id")

        imagga_api_key: str = credentials.credentials.get("IMAGGA_API_KEY")
        imagga_api_secret: str = credentials.credentials.get("IMAGGA_API_SECRET")
        key = f"{imagga_api_key}:{imagga_api_secret}"
        encoded_key = base64.b64encode(key.encode()).decode()

        headers = {"Authorization": f"Basic {encoded_key}"}

        api_url = f"https://api.imagga.com/v2/faces/similarity?face_id={face_id}&second_face_id={second_face_id}"

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    score = data.get("result", {}).get("score", 0)
                    return PluginOutput(data={"score": score})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
