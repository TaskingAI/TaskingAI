import base64
from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class VectorizerAi(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        vectorizer_api_id: str = credentials.credentials.get("VECTORIZER_API_ID")
        vectorizer_api_secret: str = credentials.credentials.get("VECTORIZER_API_SECRET")
        image_url: str = "https://imagedelivery.net/-NqW7GztWRvGPFGeAQjQpQ/b73e8910-2c6b-49dc-7021-5771c1154a00/public"
        mode: str = "test"

        key = f"{vectorizer_api_id}:{vectorizer_api_secret}"
        encoded_key = base64.b64encode(key.encode("utf-8")).decode("utf-8")
        headers = {"Authorization": f"Basic {encoded_key}"}

        api_url = "https://api.vectorizer.ai/api/v1/vectorize"

        body = {
            "image.url": image_url,
            "mode": mode,
        }

        async with ClientSession() as session:
            async with session.post(url=api_url, headers=headers, json=body, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
