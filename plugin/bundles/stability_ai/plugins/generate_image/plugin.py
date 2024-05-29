import json

from aiohttp import ClientSession

from app.service.image_storage import save_base64_image_to_s3_or_local
from bundle_dependency import *
from config import CONFIG


class GenerateImage(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        prompt: str = plugin_input.input_params.get("prompt")
        engine_id: str = plugin_input.input_params.get("engine_id", "stable-diffusion-v1-6")
        steps: int = plugin_input.input_params.get("steps", 30)
        cfg_scale: int = plugin_input.input_params.get("cfg_scale", 7)
        height: int = plugin_input.input_params.get("height", 512)
        width: int = plugin_input.input_params.get("width", 512)
        project_id: str = plugin_input.project_id

        if not project_id:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "project_id is required")

        if height % 64 != 0 or width % 64 != 0:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "height and width must be multiples of 64")

        if height < 128 or width < 128:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "height and width must both be at least 128")

        stability_ai_api_key: str = credentials.credentials.get("STABILITY_AI_API_KEY")

        url = f"https://api.stability.ai/v1/generation/{engine_id}/text-to-image"

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {stability_ai_api_key}"}

        data = {
            "text_prompts": [{"text": prompt}],
            "steps": steps,
            "cfg_scale": cfg_scale,
            "height": height,
            "width": width,
            "samples": 1,
        }

        async with ClientSession() as session:
            async with session.post(url=url, headers=headers, json=data, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    base64_image = data["artifacts"][0]["base64"]
                    format = "png"
                    image_url = await save_base64_image_to_s3_or_local(
                        base64_image_string=base64_image,
                        project_id=project_id,
                        file_format=format,
                        plugin_id="stability_ai/generate_image",
                    )
                    return PluginOutput(data={"image_url": image_url})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
