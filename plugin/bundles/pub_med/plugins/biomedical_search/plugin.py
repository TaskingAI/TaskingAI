import json
import xmltodict
from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class BiomedicalSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        pub_year: str = plugin_input.input_params.get("pub_year")
        journal: str = plugin_input.input_params.get("journal")
        pub_med_api_key: str = credentials.credentials.get("PUB_MED_API_KEY")

        edit_query = "+".join(query.split())

        esearch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?retmode=json&db=pubmed&api_key={pub_med_api_key}&term={edit_query}"

        if journal:
            esearch_url += f"+AND+{journal}[journal]"
        if pub_year:
            esearch_url += f"+AND+{pub_year}[pdat]"

        async with ClientSession() as session:
            async with session.get(url=esearch_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    search_data = data.get("esearchresult", {}).get("idlist", [])
                    edit_data = ",".join(search_data)

                    efetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&api_key={pub_med_api_key}&id={edit_data}"
                    async with session.get(url=efetch_url, proxy=CONFIG.PROXY) as fetch_response:
                        if fetch_response.status == 200:
                            data = await fetch_response.text()
                            data_in_json = xmltodict.parse(data)
                            contents = data_in_json.get("PubmedArticleSet", {}).get("PubmedArticle", {})
                        else:
                            data = await fetch_response.json()
                            raise_provider_api_error(json.dumps(data))

                    elink_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?retmode=json&dbfrom=pubmed&api_key={pub_med_api_key}&cmd=llinks&id={edit_data}"
                    async with session.get(url=elink_url, proxy=CONFIG.PROXY) as link_response:
                        if link_response.status == 200:
                            data = await link_response.json()
                            link_data = data.get("linksets", {})[0].get("idurllist")
                        else:
                            data = await link_response.json()
                            raise_provider_api_error(json.dumps(data))

                    combined_data = []
                    for content, links in zip(contents, link_data):
                        urls = []
                        if not links.get("info"):
                            for link in links.get("objurls", []):
                                urls.append(link.get("url", {}).get("value", ""))

                        combined_data.append(
                            {
                                "id": content.get("MedlineCitation", {}).get("PMID", {}).get("#text", ""),
                                "title": content.get("MedlineCitation", {}).get("Article", {}).get("ArticleTitle", ""),
                                "abstract": content.get("MedlineCitation", {})
                                .get("Article", {})
                                .get("Abstract", {})
                                .get("AbstractText", ""),
                                "url": urls,
                            }
                        )
                    return PluginOutput(data={"results": json.dumps(combined_data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
