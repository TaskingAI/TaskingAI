from provider_dependency.text_embedding import *


cohere_input_type_map = {
    TextEmbeddingInputType.document: "search_document",
    TextEmbeddingInputType.query: "search_query",
}


class CohereTextEmbeddingModel(BaseTextEmbeddingModel):

    API_URL = "https://api.cohere.ai/v1/embed"

    async def embed_text(
        self,
        provider_model_id: str,
        input: List[str],
        credentials: ProviderCredentials,
        configs: TextEmbeddingModelConfiguration,
        input_type: Optional[TextEmbeddingInputType] = None,
    ) -> TextEmbeddingResult:
        headers = {
            "Authorization": f"Bearer {credentials.COHERE_API_KEY}",
            "Content-Type": "application/json",
        }
        if input_type is None:
            input_type = TextEmbeddingInputType.document
        cohere_input_type = cohere_input_type_map[input_type]

        payload = {
            "model": provider_model_id,
            "texts": input,
            "input_type": cohere_input_type,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.API_URL, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                await self.handle_response(response)
                response_json = await response.json()
                return TextEmbeddingResult(
                    data=[
                        TextEmbeddingOutput(embedding=output, index=i)
                        for i, output in enumerate(response_json["embeddings"])
                    ],
                )
