from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class SemanticScholar(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        semantic_scholar_api_key: str = (
            credentials.credentials.get("SEMANTIC_SCHOLAR_API_KEY", None) if credentials else None
        )

        if not semantic_scholar_api_key:
            pass
        else:
            api_url = "https://api.semanticscholar.org/graph/v1/paper/search?query=artificial intelligence&limit=1&fields=title,venue,url,year,authors,abstract,isOpenAccess,openAccessPdf,publicationTypes,publicationDate,journal,fieldsOfStudy"
            headers = {"x-api-key": semantic_scholar_api_key}
            async with ClientSession() as session:
                async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                    if response.status == 200:
                        pass
                    else:
                        raise_credentials_validation_error()
