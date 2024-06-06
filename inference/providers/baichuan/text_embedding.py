from provider_dependency.text_embedding import *


class BaichuanTextEmbeddingModel(BaseTextEmbeddingModel):
    async def embed_text(
        self,
        provider_model_id: str,
        input: List[str],
        credentials: ProviderCredentials,
        configs: TextEmbeddingModelConfiguration,
        input_type: Optional[TextEmbeddingInputType] = None,
    ) -> TextEmbeddingResult:

        api_url = "https://api.baichuan-ai.com/v1/embeddings"

        headers = {
            "Authorization": f"Bearer {credentials.BAICHUAN_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": provider_model_id,
            "input": input,
            "encoding_format": "float",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                await self.handle_response(response)
                response_json = await response.json()
                return TextEmbeddingResult(
                    data=[
                        TextEmbeddingOutput(embedding=output["embedding"], index=output["index"])
                        for output in response_json["data"]
                    ],
                )
