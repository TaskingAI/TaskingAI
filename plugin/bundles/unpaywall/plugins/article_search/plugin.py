import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class ArticleSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        email: str = plugin_input.input_params.get("email")
        page: int = plugin_input.input_params.get("page", None)

        api_url = f"https://api.unpaywall.org/v2/search?query={query}&email={email}"

        if page:
            api_url += f"&page={page}"

        async with ClientSession() as session:
            async with session.get(url=api_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("results")
                    final_data = []
                    for result in results:
                        final_data.append(
                            {
                                "title": result.get("response").get("title"),
                                "published_date": result.get("response").get("published_date"),
                                "authors": result.get("response").get("z_authors"),
                                "journal_name": result.get("response").get("journal_name"),
                                "doi": result.get("response").get("doi"),
                                "doi_url": result.get("response").get("doi_url"),
                                "oa_status": result.get("response").get("is_oa"),
                                "oa_url": result.get("response").get("oa_locations"),
                                "publisher": result.get("response").get("publisher"),
                            }
                        )
                    return PluginOutput(data={"results": json.dumps(final_data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
