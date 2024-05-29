from provider_dependency.text_embedding import *


class MistralaiTextEmbeddingModel(BaseTextEmbeddingModel):

    API_URL = "https://api.mistral.ai/v1/embeddings"

    async def embed_text(
        self,
        provider_model_id: str,
        input: List[str],
        credentials: ProviderCredentials,
        configs: TextEmbeddingModelConfiguration,
        input_type: Optional[TextEmbeddingInputType] = None,
    ) -> TextEmbeddingResult:

        headers = {
            "Authorization": f"Bearer {credentials.MISTRAL_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": provider_model_id,
            "input": input,
            "encoding_format": "float",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.API_URL, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                await self.handle_response(response)
                response_json = await response.json()
                return TextEmbeddingResult(
                    data=[
                        TextEmbeddingOutput(embedding=output["embedding"], index=output["index"])
                        for output in response_json["data"]
                    ],
                )
