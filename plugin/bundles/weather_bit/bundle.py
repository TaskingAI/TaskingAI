from aiohttp import ClientSession

from bundle_dependency import *


class WeatherBit(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        WEATHER_BIT_API_KEY: str = credentials.credentials.get("WEATHER_BIT_API_KEY")
        lat: float = 30.25
        lon: float = 120.166

        url = f"https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&units=M&key={WEATHER_BIT_API_KEY}"

        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
