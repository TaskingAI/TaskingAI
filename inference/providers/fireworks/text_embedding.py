from provider_dependency.text_embedding import *
from typing import List, Dict, Optional


class FireworksTextEmbeddingModel(BaseTextEmbeddingModel):
    async def embed_text(
        self,
        provider_model_id: str,
        input: List[str],
        credentials: ProviderCredentials,
        configs: TextEmbeddingModelConfiguration,
        input_type: Optional[TextEmbeddingInputType] = None,
        proxy: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> TextEmbeddingResult:
        api_url = "https://api.fireworks.ai/inference/v1/embeddings"

        headers = _build_fireworks_header(credentials)

        payload = {"model": provider_model_id, "input": input}

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


def _build_fireworks_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.FIREWORKS_API_KEY}",
        "Content-Type": "application/json",
    }
