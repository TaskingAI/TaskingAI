import urllib.parse

from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class TripAdvisor(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        query: str = "Italian food in New York"
        category: str = "restaurants"
        TRIP_ADVISOR_API_KEY: str = credentials.credentials.get("TRIP_ADVISOR_API_KEY")

        query = urllib.parse.quote_plus(query)
        url = f"https://api.content.tripadvisor.com/api/v1/location/search?key={TRIP_ADVISOR_API_KEY}&searchQuery={query}"

        if category:
            url += f"&category={category}"

        async with ClientSession() as session:
            async with session.get(url=url, headers={"accept": "application/json"}, proxy=CONFIG.PROXY) as response:

                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()