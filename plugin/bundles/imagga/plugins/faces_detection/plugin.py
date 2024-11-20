import json
import base64

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class FacesDetection(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        image_url: str = plugin_input.input_params.get("image_url")
        return_face_id: int = plugin_input.input_params.get("return_face_id", None)

        imagga_api_key: str = credentials.credentials.get("IMAGGA_API_KEY")
        imagga_api_secret: str = credentials.credentials.get("IMAGGA_API_SECRET")
        key = f"{imagga_api_key}:{imagga_api_secret}"
        encoded_key = base64.b64encode(key.encode()).decode()

        headers = {"Authorization": f"Basic {encoded_key}"}

        api_url = f"https://api.imagga.com/v2/faces/detections?image_url={image_url}"

        if return_face_id:
            api_url += f"&return_face_id={return_face_id}"

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"result": json.dumps(data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
