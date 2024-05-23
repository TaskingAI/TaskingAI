from provider_dependency.text_embedding import *


class HuggingFaceInferenceEndpointTextEmbeddingModel(BaseTextEmbeddingModel):
    async def embed_text(
        self,
        provider_model_id: str,
        input: List[str],
        credentials: ProviderCredentials,
        configs: TextEmbeddingModelConfiguration,
        input_type: Optional[TextEmbeddingInputType] = None,
    ) -> TextEmbeddingResult:
        api_url = credentials.HUGGING_INFERENCE_ENDPOINT_URL

        headers = {
            "Authorization": f"Bearer {credentials.HUGGING_FACE_API_KEY}",
            "Content-Type": "application/json",
        }

        outputs = []
        for i, text in enumerate(input):
            payload = {
                "parameters": {},
                "inputs": text,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                    await self.handle_response(response)
                    response_json = await response.json()
                    outputs.append(TextEmbeddingOutput(embedding=response_json["embeddings"], index=i))

        return TextEmbeddingResult(data=outputs)
