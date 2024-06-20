from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class PubMed(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        pub_med_api_key: str = credentials.credentials.get("PUB_MED_API_KEY")
        query: str = "breast cancer"
        edit_query = "+".join(query.split())

        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?retmode=json&db=pubmed&term={edit_query}&api_key={pub_med_api_key}"

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
