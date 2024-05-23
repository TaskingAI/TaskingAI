from provider_dependency.rerank import *


class CohereRerankModel(BaseRerankModel):

    API_URL = "https://api.cohere.ai/v1/rerank"

    async def rerank(
        self,
        provider_model_id: str,
        credentials: ProviderCredentials,
        query: str,
        documents: List[str],
        top_n: int,
    ) -> RerankResult:

        headers = {
            "Authorization": f"Bearer {credentials.COHERE_API_KEY}",
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
                results = []
                for item in response_json["results"]:
                    if item["index"] < len(documents):  # Ensure the index is within bounds
                        doc_text = documents[item["index"]]
                        doc = Document(text=doc_text)
                        rerank_doc = RerankDocument(
                            index=item["index"], document=doc, relevance_score=item["relevance_score"]
                        )
                        results.append(rerank_doc)
                    else:
                        # Handle the case where index is out of bounds
                        raise_http_error(
                            ErrorCode.PROVIDER_ERROR,
                            f"Index {item['index']} is out of bounds for documents of length {len(documents)}.",
                        )
                return RerankResult(results=results)
