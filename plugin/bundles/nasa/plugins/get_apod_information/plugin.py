import json
from aiohttp import ClientSession
from bundle_dependency import *
from config import CONFIG


class GetApodInformation(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        NASA_API_KEY: str = credentials.credentials.get("NASA_API_KEY")
        input_params = plugin_input.input_params or {}

        date: str = input_params.get("date")
        start_date: str = input_params.get("start_date")
        end_date: str = input_params.get("end_date")
        count: int = input_params.get("count")
        thumbs: bool = input_params.get("thumbs")

        base_url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"

        if date:
            base_url += f"&date={date}"
        elif start_date:
            base_url += f"&start_date={start_date}"
            if end_date:
                base_url += f"&end_date={end_date}"
        elif count:
            base_url += f"&count={count}"
        if thumbs:
            base_url += f"&thumbs={thumbs}"

        async with ClientSession() as session:
            async with session.get(base_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()

                    if isinstance(data, list):
                        images = data
                    else:
                        images = [data]

                    astronomical_images = []
                    for image in images:
                        astronomical_images.append(
                            {
                                "date": image.get("date", ""),
                                "title": image.get("title", ""),
                                "explanation": image.get("explanation", ""),
                                "url": image.get("url", ""),
                            }
                        )
                    return PluginOutput(data={"result": json.dumps(astronomical_images)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
