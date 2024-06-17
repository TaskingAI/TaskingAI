import json

import aiohttp

from bundle_dependency import *
from config import CONFIG

TRANSCRIBE_API_URL = f"https://api.transcribetube.com/api/transcribeVideo"
LIST_API_URL = f"https://api.transcribetube.com/api/list"
DETAIL_API_URL = f"https://api.transcribetube.com/api/detail/"


class VideoTranscribe(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        web_url: str = plugin_input.input_params.get("web_url")
        video_id: str = plugin_input.input_params.get("id")
        language: str = plugin_input.input_params.get("language")
        youtube_transcribe_api_key: str = credentials.credentials.get("YOUTUBE_TRANSCRIBE_API_KEY", "")

        headers = {"api-key": youtube_transcribe_api_key}

        payload = {"language": language, "webhookUrl": web_url, "youtubeVideoId": video_id}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=TRANSCRIBE_API_URL, headers=headers, json=payload, proxy=CONFIG.PROXY
            ) as response:
                if response.status == 201:
                    async with session.get(url=LIST_API_URL, headers=headers, proxy=CONFIG.PROXY) as list_response:
                        if list_response.status == 200:
                            data = await list_response.json()
                            for item in data:
                                if not item["youtubeId"] == video_id:
                                    continue

                                project_id = item.get("_id")
                                async with session.get(
                                    url=DETAIL_API_URL + project_id, headers=headers, proxy=CONFIG.PROXY
                                ) as detail_response:
                                    if detail_response.status == 200:
                                        data = await detail_response.json()
                                        title = data.get("name", "")
                                        transcription = data.get("transcription", "")
                                        transcription_text = ""
                                        for paragraph in transcription:
                                            for word in paragraph.get("children", ""):
                                                transcription_text += word.get("text", "")

                                        return PluginOutput(
                                            data={
                                                "results": json.dumps(
                                                    {"title": title, "transcription": transcription_text}
                                                )
                                            }
                                        )
                                    else:
                                        data = await detail_response.json()
                                        raise_provider_api_error(json.dumps(data))
                        else:
                            data = await list_response.json()
                            raise_provider_api_error(json.dumps(data))
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
