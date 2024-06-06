from provider_dependency.text_embedding import *
from typing import List, Dict


class GoogleGeminiTextEmbeddingModel(BaseTextEmbeddingModel):
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

        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{provider_model_id}:embedContent"

        headers = _build_google_gemini_header(credentials)
        if proxy:
            if not proxy.startswith("https://"):
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid proxy URL. Must start with https://")
            # complete the proxy if not end with /
            api_url = proxy

        if custom_headers:
            headers.update(custom_headers)

        parts = []
        payload = {"content": {"parts": parts}}
        for i, text in enumerate(input):
            part = {"text": text}
            parts.append(part)
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                await self.handle_response(response)
                response_json = await response.json()
                outputs = TextEmbeddingResult(
                    data=[TextEmbeddingOutput(embedding=response_json["embedding"]["values"], index=0)],
                )

        return outputs


def _build_google_gemini_header(credentials: ProviderCredentials):
    return {
        "x-goog-api-key": f" {credentials.GOOGLE_GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }
