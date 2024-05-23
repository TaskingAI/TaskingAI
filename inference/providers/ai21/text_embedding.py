from provider_dependency.text_embedding import *


class Ai21TextEmbeddingModel(BaseTextEmbeddingModel):
    async def embed_text(
        self,
        provider_model_id: str,
        input: List[str],
        credentials: ProviderCredentials,
        configs: TextEmbeddingModelConfiguration,
        input_type: Optional[TextEmbeddingInputType] = None,
    ) -> TextEmbeddingResult:

        api_url = "https://api.ai21.com/studio/v1/embed"

        headers = {
            "Authorization": f"Bearer {credentials.AI21_API_KEY}",
            "Content-Type": "application/json",
        }

        trimmed_input = [item[:2000] for item in input]

        payload = {"texts": trimmed_input}

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                await self.handle_response(response)
                response_json = await response.json()
                return TextEmbeddingResult(
                    data=[
                        TextEmbeddingOutput(embedding=response_json["results"][i]["embedding"], index=i)
                        for i in range(len(response_json["results"]))
                    ],
                )
