import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GetSportTeams(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        sport: str = plugin_input.input_params.get("sport")

        sport_dict = {
            "ncaa football": 1,
            "nfl": 2,
            "mlb": 3,
            "nba": 4,
            "ncaa men's basketball": 5,
            "nhl": 6,
            "ufc/mma": 7,
            "wnba": 8,
            "mls": 10,
            "epl": 11,
            "fra1": 12,
            "ger1": 13,
            "esp1": 14,
            "ita1": 15,
            "uefachamp": 16,
            "uefaeuro": 17,
            "fifa": 18,
            "jpn1": 19,
            "ipl": 20,
            "t20": 21,
        }

        if sport.lower() in sport_dict:
            sport: int = sport_dict.get(sport.lower())
        else:
            raise ValueError(f"invalid sport: {sport}")

        api_url = f"https://api.apilayer.com/therundown/sports/{sport}/teams"

        headers = {"apikey": credentials.credentials.get("RUNDOWN_API_API_KEY")}

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"results": json.dumps(data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
