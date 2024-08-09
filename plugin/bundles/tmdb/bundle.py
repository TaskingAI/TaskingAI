from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Tmdb(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        TMDB_API_KEY: str = credentials.credentials.get("TMDB_API_KEY")
        sort_by = "popularity.desc"

        api_url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&sort_by={sort_by}"

        async with ClientSession() as session:
            async with session.get(url=api_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
