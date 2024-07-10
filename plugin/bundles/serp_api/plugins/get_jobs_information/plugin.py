import json

from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class GetJobsInformation(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        SERP_API_API_KEY: str = credentials.credentials.get("SERP_API_API_KEY")
        q: str = plugin_input.input_params.get("q")
        hl: str = plugin_input.input_params.get("hl")
        gl: str = plugin_input.input_params.get("gl")

        base_url = f"https://serpapi.com/search?engine=google_jobs&q={q}&api_key={SERP_API_API_KEY}"
        if hl:
            base_url += f"&hl={hl}"
        if gl:
            base_url += f"&gl={gl}"

        async with ClientSession() as session:
            async with session.get(base_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    jobs_results = data.get("jobs_results", {})
                    job_info = []

                    for job in jobs_results:
                        job_info.append(
                            {
                                "title": job.get("title", ""),
                                "company_name": job.get("company_name", ""),
                                "location": job.get("location", ""),
                                "description": job.get("description", ""),
                                "job_highlights": job.get("job_highlights", ""),
                                "extensions": job.get("extensions", ""),
                            }
                        )

                    return PluginOutput(data={"result": json.dumps(job_info)})

                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
