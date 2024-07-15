from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Nasa(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        NASA_API_KEY: str = credentials.credentials.get("NASA_API_KEY")
        date: str = "2024-07-14"
        base_url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date}"

        async with ClientSession() as session:
            async with session.get(base_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
