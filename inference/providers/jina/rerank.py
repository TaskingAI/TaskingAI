from provider_dependency.rerank import *
from typing import Optional, List, Dict


class JinaRerankModel(BaseRerankModel):
    API_URL = "https://api.jina.ai/v1/rerank"

    async def rerank(
        self,
        provider_model_id: str,
        credentials: ProviderCredentials,
        query: str,
        documents: List[str],
        top_n: int,
        proxy: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> RerankResult:
        api_url = self.API_URL
        headers = {
            "Authorization": f"Bearer {credentials.JINA_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": provider_model_id,
            "query": query,
            "documents": documents,
            "top_n": top_n,
        }

        if proxy:
            if not proxy.startswith("https://"):
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid proxy URL. Must start with https://")
            # complete the proxy if not end with /
            api_url = proxy

        if custom_headers:
            headers.update(custom_headers)
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                await self.handle_response(response)
                response_json = await response.json()
                return RerankResult(
                    results=response_json["results"],
                )
