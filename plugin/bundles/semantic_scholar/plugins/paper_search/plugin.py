import json
from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class PaperSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        publication_date_or_year: str = plugin_input.input_params.get("publication_date_or_year", None)
        open_access_pdf: bool = plugin_input.input_params.get("open_access_pdf", None)
        offset: int = plugin_input.input_params.get("offset", None)
        limit: int = plugin_input.input_params.get("limit", None)

        semantic_scholar_api_key: str = (
            credentials.credentials.get("SEMANTIC_SCHOLAR_API_KEY", None) if credentials else None
        )

        api_url = f"https://api.semanticscholar.org/graph/v1/paper/search?fields=title,url,year,authors,abstract,isOpenAccess,openAccessPdf,publicationTypes,publicationDate,journal,fieldsOfStudy&query={query}"

        headers = {"x-api-key": semantic_scholar_api_key} if semantic_scholar_api_key else None
        if publication_date_or_year:
            api_url += f"&publicationDateOrYear={publication_date_or_year}"
        if open_access_pdf:
            api_url += f"&openAccessPdf"
        if offset:
            api_url += f"&offset={offset}"
        if limit:
            api_url += f"&limit={limit}"

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("data", [])
                    optimized_items = []
                    for item in items:
                        optimized_items.append(
                            {
                                "title": item["title"],
                                "url": item["url"],
                                "year": item["year"],
                                "authors": item["authors"],
                                "abstract": item["abstract"],
                                "isOpenAccess": item["isOpenAccess"],
                                "openAccessPdf": item["openAccessPdf"],
                                "publicationTypes": item["publicationTypes"],
                                "publicationDate": item["publicationDate"],
                                "journal": item["journal"],
                                "fieldsOfStudy": item["fieldsOfStudy"],
                            }
                        )

                    return PluginOutput(data={"result": json.dumps(optimized_items)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
