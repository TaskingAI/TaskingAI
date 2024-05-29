from aiohttp import ClientSession

from bundle_dependency import *


class OpenWeather(BundleHandler):

    async def verify(self, credentials: BundleCredentials):
        # todo: implement with actual verification logic
        lat: float = 30.25
        lon: float = 120.166

        base_url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            'lat': lat,
            'lon': lon,
            'exclude': 'minutely,hourly,daily,alerts',
            'appid': credentials.credentials.get("OPEN_WEATHER_API_KEY", ""),
            'units': 'metric'
        }
        async with ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()




