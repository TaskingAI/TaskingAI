from provider_dependency.rerank import *


class JinaRerankModel(BaseRerankModel):

    API_URL = "https://api.jina.ai/v1/rerank"

    async def rerank(
        self,
        provider_model_id: str,
        credentials: ProviderCredentials,
        query: str,
        documents: List[str],
        top_n: int,
    ) -> RerankResult:

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

        async with aiohttp.ClientSession() as session:
            async with session.post(self.API_URL, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                await self.handle_response(response)
                response_json = await response.json()
                return RerankResult(
                    results=response_json["results"],
                )
