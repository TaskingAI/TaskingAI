from provider_dependency.text_embedding import *
from typing import List, Dict, Optional


class CustomHostTextEmbeddingModel(BaseTextEmbeddingModel):
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
            "Authorization": f"Bearer {credentials.CUSTOM_HOST_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": credentials.CUSTOM_HOST_MODEL_ID,
            "input": input,
            "encoding_format": "float",
        }
        api_url = credentials.CUSTOM_HOST_ENDPOINT_URL
        for url in CONFIG.PROVIDER_URL_BLACK_LIST:
            if url in api_url:
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"Invalid provider url: {url}")

        if not (api_url.startswith("http://") or api_url.startswith("https://")):
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR,
                f"Invalid provider url: {api_url}, must start with http:// or https://",
            )
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
                        TextEmbeddingOutput(embedding=output["embedding"], index=output["index"])
                        for output in response_json["data"]
                    ],
                )
