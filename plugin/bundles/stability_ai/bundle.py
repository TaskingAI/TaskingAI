from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class StabilityAi(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        prompt: str = "a cartoon styled image of a cat playing tennis against a dog"
        engine_id: str = "stable-diffusion-v1-6"
        steps: int = 30
        cfg_scale: int = 7
        height: int = 512
        width: int = 512

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
                    pass
                else:
                    raise_credentials_validation_error()
