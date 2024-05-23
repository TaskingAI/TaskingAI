from provider_dependency.text_embedding import *


class JinaTextEmbeddingModel(BaseTextEmbeddingModel):

    API_URL = "https://api.jina.ai/v1/embeddings"

    async def embed_text(
        self,
        provider_model_id: str,
        input: List[str],
        credentials: ProviderCredentials,
        configs: TextEmbeddingModelConfiguration,
        input_type: Optional[TextEmbeddingInputType] = None,
    ) -> TextEmbeddingResult:

        headers = {
            "Authorization": f"Bearer {credentials.JINA_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": provider_model_id,
            "input": input,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.API_URL, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                await self.handle_response(response)
                response_json = await response.json()
                return TextEmbeddingResult(
                    data=[
                        TextEmbeddingOutput(embedding=output["embedding"], index=i)
                        for i, output in enumerate(response_json["data"])
                    ],
                )
