from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class SerpApi(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        SERP_API_API_KEY: str = credentials.credentials.get("SERP_API_API_KEY")
        departure_id: str = "CDG"
        arrival_id: str = "AUS"
        outbound_date: str = "2024-07-30"
        type: int = 2

        base_url = f"https://serpapi.com/search?engine=google_flights&departure_id={departure_id}&arrival_id={arrival_id}&outbound_date={outbound_date}&api_key={SERP_API_API_KEY}&type={type}"
        async with ClientSession() as session:
            async with session.get(base_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
