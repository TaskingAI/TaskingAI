import json

from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Text2Image(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        model: str = plugin_input.input_params.get("model", None)
        prompt: str = plugin_input.input_params.get("prompt")
        negative_prompt: str = plugin_input.input_params.get("negative_prompt", None)
        width: int = plugin_input.input_params.get("width", None)
        height: int = plugin_input.input_params.get("height", None)
        steps: int = plugin_input.input_params.get("steps", None)
        guidance: float = plugin_input.input_params.get("guidance", None)
        seed: int = plugin_input.input_params.get("seed", None)
        scheduler: str = plugin_input.input_params.get("scheduler", None)
        output_format: str = plugin_input.input_params.get("output_format", None)
        response_format: str = plugin_input.input_params.get("response_format", None)

        getimg_api_key: str = credentials.credentials.get("GETIMG_API_KEY")

        api_url = "https://api.getimg.ai/v1/stable-diffusion/text-to-image"

        headers = {"accept": "application/json", "Authorization": f"Bearer {getimg_api_key}"}

        payload = {
            "prompt": prompt,
        }

        if model:
            payload["model"] = model

        if negative_prompt:
            payload["negative_prompt"] = negative_prompt

        if width:
            payload["width"] = width

        if height:
            payload["height"] = height

        if steps:
            payload["steps"] = steps

        if guidance:
            payload["guidance"] = guidance

        if seed:
            payload["seed"] = seed

        if scheduler:
            payload["scheduler"] = scheduler

        if output_format:
            payload["output_format"] = output_format

        if response_format:
            payload["response_format"] = response_format

        async with ClientSession() as session:
            async with session.post(url=api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    result = await response.json()
                    if response_format and response_format == "url":
                        return PluginOutput(data={"result": result.get("url")})
                    return PluginOutput(data={"result": json.dumps(result.get("image"))})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
