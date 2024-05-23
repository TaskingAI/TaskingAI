from provider_dependency.text_embedding import *


class OllamaTextEmbeddingModel(BaseTextEmbeddingModel):
    async def embed_text(
        self,
        provider_model_id: str,
        input: List[str],
        credentials: ProviderCredentials,
        configs: TextEmbeddingModelConfiguration,
        input_type: Optional[TextEmbeddingInputType] = None,
    ) -> TextEmbeddingResult:

        api_url = build_url(credentials.OLLAMA_HOST, "/api/embeddings")

        headers = {
            "Content-Type": "application/json",
        }

        outputs = []
        for i, text in enumerate(input):
            payload = {
                "model": provider_model_id,
                "prompt": text,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                    await self.handle_response(response)
                    response_json = await response.json()
                    outputs.append(TextEmbeddingOutput(embedding=response_json["embedding"], index=i))

        return TextEmbeddingResult(data=outputs)
