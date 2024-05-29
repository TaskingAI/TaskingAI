from provider_dependency.text_embedding import *
from typing import List, Dict, Optional


class OpenaiTextEmbeddingModel(BaseTextEmbeddingModel):
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
        api_url = "https://api.openai.com/v1/embeddings"

        headers = {
            "Authorization": f"Bearer {credentials.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": provider_model_id,
            "input": input,
            "encoding_format": "float",
        }
        if proxy:
            if not proxy.startswith("https://"):
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid proxy URL. Must start with https://")
            # complete the proxy if not end with /
            api_url = proxy

        if custom_headers:
            headers.update(custom_headers)

        if provider_model_id == "text-embedding-3-small-512":
            payload["dimensions"] = 512
            payload["model"] = "text-embedding-3-small"
        elif provider_model_id == "text-embedding-3-small-1536":
            payload["dimensions"] = 1536
            payload["model"] = "text-embedding-3-small"
        elif provider_model_id == "text-embedding-3-large-256":
            payload["dimensions"] = 256
            payload["model"] = "text-embedding-3-large"
        elif provider_model_id == "text-embedding-3-large-1024":
            payload["dimensions"] = 1024
            payload["model"] = "text-embedding-3-large"

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
