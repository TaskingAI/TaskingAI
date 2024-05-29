from provider_dependency.text_embedding import *


class HuggingFaceTextEmbeddingModel(BaseTextEmbeddingModel):
    async def embed_text(
        self,
        provider_model_id: str,
        input: List[str],
        credentials: ProviderCredentials,
        configs: TextEmbeddingModelConfiguration,
        input_type: Optional[TextEmbeddingInputType] = None,
    ) -> TextEmbeddingResult:

        base_url = "https://api-inference.huggingface.co/models/PLACE_HOLDER_MODEL_ID"
        api_url = base_url.replace("PLACE_HOLDER_MODEL_ID", provider_model_id)

        headers = {
            "Authorization": f"Bearer {credentials.HUGGING_FACE_API_KEY}",
            "Content-Type": "application/json",
        }

        outputs = []
        for i, text in enumerate(input):
            payload = {
                "inputs": text,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                    await self.handle_response(response)
                    response_json = await response.json()
                    outputs.append(TextEmbeddingOutput(embedding=response_json, index=i))

        return TextEmbeddingResult(data=outputs)
