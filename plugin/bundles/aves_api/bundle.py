from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class AvesApi(BundleHandler):
    async def verify(self, credentials: BundleCredentials):

        aves_api_api_key: str = credentials.credentials.get("AVES_API_API_KEY")
        query: str = "today's google doodle"
        type: str = "web"

        api_url = f"https://api.avesapi.com/search?apikey={aves_api_api_key}&query={query}&type={type}"

        async with ClientSession() as session:
            async with session.get(url=api_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
