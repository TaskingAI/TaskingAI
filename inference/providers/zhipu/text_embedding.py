from provider_dependency.text_embedding import *
from .utils import build_zhipu_header


class ZhipuTextEmbeddingModel(BaseTextEmbeddingModel):
    async def embed_text(
        self,
        provider_model_id: str,
        input: List[str],
        credentials: ProviderCredentials,
        configs: TextEmbeddingModelConfiguration,
        input_type: Optional[TextEmbeddingInputType] = None,
    ) -> TextEmbeddingResult:

        api_url = "https://open.bigmodel.cn/api/paas/v4/embeddings"

        headers = build_zhipu_header(credentials)

        outputs = []
        for i, text in enumerate(input):
            payload = {
                "model": provider_model_id,
                "input": text,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                    await self.handle_response(response)
                    response_json = await response.json()
                    outputs.append(TextEmbeddingOutput(embedding=response_json["data"][0]["embedding"], index=i))

        return TextEmbeddingResult(data=outputs)
