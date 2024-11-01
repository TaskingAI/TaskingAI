from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class NovitaAi(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        model_name: str = "sd_xl_base_1.0.safetensors"
        novita_api_key: str = credentials.credentials.get("NOVITA_API_KEY")
        prompt: str = "a cute dog"
        width: int = 512
        height: int = 512
        image_num: int = 1
        steps: int = 20
        guidance_scale: float = 7.5
        sampler_name: str = "Euler a"
        negative_prompt: str = "nsfw, bottle, bad face"
        seed: int = 123

        api_url = "https://api.novita.ai/v3/async/txt2img"

        headers = {"Authorization": f"Bearer {novita_api_key}", "Content-Type": "application/json"}

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
                "negative_prompt": negative_prompt,
                "seed": seed,
            }
        }

        async with ClientSession() as session:
            async with session.post(url=api_url, headers=headers, json=data, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
