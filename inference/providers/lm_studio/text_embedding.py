from provider_dependency.text_embedding import *


class LmStudioTextEmbeddingModel(BaseTextEmbeddingModel):
    async def embed_text(
        self,
        provider_model_id: str,
        input: List[str],
        credentials: ProviderCredentials,
        configs: TextEmbeddingModelConfiguration,
        input_type: Optional[TextEmbeddingInputType] = None,
    ) -> TextEmbeddingResult:

        api_url = credentials.LM_STUDIO_HOST

        headers = {
            "Content-Type": "application/json",
        }

        payload = {
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
