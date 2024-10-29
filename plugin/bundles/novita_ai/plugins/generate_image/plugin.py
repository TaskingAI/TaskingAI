import json
import asyncio
from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class GenerateImage(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        model_name: str = plugin_input.input_params.get("model_name", "sd_xl_base_1.0.safetensors")
        prompt: str = plugin_input.input_params.get("prompt")
        width: int = plugin_input.input_params.get("width")
        height: int = plugin_input.input_params.get("height")
        image_num: int = plugin_input.input_params.get("image_num")
        steps: int = plugin_input.input_params.get("steps")
        guidance_scale: float = plugin_input.input_params.get("guidance_scale")
        sampler_name: str = plugin_input.input_params.get("sampler_name")
        negative_prompt: str = plugin_input.input_params.get("negative_prompt", None)
        seed: int = plugin_input.input_params.get("seed", None)
        response_image_type: str = plugin_input.input_params.get("response_image_type", None)

        api_url = "https://api.novita.ai/v3/async/txt2img"

        headers = {
            "Authorization": f"Bearer {credentials.credentials.get('NOVITA_API_KEY')}",
            "Content-Type": "application/json",
        }

        data = {
            "request": {
                "model_name": model_name,
                "prompt": prompt,
                "width": width,
                "height": height,
                "image_num": image_num,
                "steps": steps,
                "guidance_scale": guidance_scale,
                "sampler_name": sampler_name,
            }
        }
        if negative_prompt:
            data["request"]["negative_prompt"] = negative_prompt
        if seed:
            data["request"]["seed"] = seed
        if response_image_type:
            data["extra"]["response_image_type"] = response_image_type

        async with ClientSession() as session:
            async with session.post(
                url=api_url, headers=headers, data=json.dumps(data), proxy=CONFIG.PROXY
            ) as response_1:
                if response_1.status == 200:
                    data = await response_1.json()
                    task_id = data.get("task_id")
                    url = f"https://api.novita.ai/v3/async/task-result?task_id={task_id}"

                    await asyncio.sleep(20)

                    async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response_2:
                        if response_2.status == 200:
                            data = await response_2.json()
                            images = data.get("images", [])
                            image_url = []
                            for image in images:
                                image_url.append(image.get("image_url"))

                            return PluginOutput(data={"url": json.dumps(image_url)})
                        else:
                            data = await response_2.json()
                            raise_provider_api_error(json.dumps(data))
                else:
                    data = await response_1.json()
                    raise_provider_api_error(json.dumps(data))
