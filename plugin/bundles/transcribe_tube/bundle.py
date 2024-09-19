import aiohttp

from bundle_dependency import *


class TranscribeTube(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        youtube_transcribe_api_key: str = credentials.credentials.get("YOUTUBE_TRANSCRIBE_API_KEY")

        url = f"https://api.transcribetube.com/api/list"

        headers = {
            "api-key": f"{youtube_transcribe_api_key}",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers) as response:
                if response.status == 200:
                    pass
                else:
                    return False
