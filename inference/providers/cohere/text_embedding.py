from provider_dependency.text_embedding import *
from typing import List, Dict

cohere_input_type_map = {
    TextEmbeddingInputType.document: "search_document",
    TextEmbeddingInputType.query: "search_query",
}


class CohereTextEmbeddingModel(BaseTextEmbeddingModel):
    API_URL = "https://api.cohere.ai/v1/embed"

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
        headers = {
            "Authorization": f"Bearer {credentials.COHERE_API_KEY}",
            "Content-Type": "application/json",
        }
        if input_type is None:
            input_type = TextEmbeddingInputType.document
        cohere_input_type = cohere_input_type_map[input_type]

        payload = {
            "model": provider_model_id,
            "texts": input,
            "input_type": cohere_input_type,
        }
        api_url = self.API_URL
        if proxy:
            if not proxy.startswith("https://"):
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid proxy URL. Must start with https://")
            # complete the proxy if not end with /
            api_url = proxy

        if custom_headers:
            headers.update(custom_headers)
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                await self.handle_response(response)
                response_json = await response.json()
                return TextEmbeddingResult(
                    data=[
                        TextEmbeddingOutput(embedding=output, index=i)
                        for i, output in enumerate(response_json["embeddings"])
                    ],
                )
