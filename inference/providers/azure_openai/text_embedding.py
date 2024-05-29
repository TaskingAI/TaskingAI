from provider_dependency.text_embedding import *
from .utils import build_azure_text_url, build_azure_openai_header
from typing import List, Dict, Optional


class AzureOpenaiTextEmbeddingModel(BaseTextEmbeddingModel):
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
        headers = build_azure_openai_header(credentials)
        payload = {
            "model": provider_model_id,
            "input": input,
            "encoding_format": "float",
        }
        api_url = build_azure_text_url(credentials)
        if proxy:
            if not proxy.startswith("https://"):
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid proxy URL. Must start with https://")
            # complete the proxy if not end with /
            api_url = proxy

        if custom_headers:
            headers.update(custom_headers)
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload, proxy=CONFIG.PROXY) as response:
                response_json = await response.json()
                if response.status != 200:
                    raise_http_error(
                        ErrorCode.PROVIDER_ERROR,
                        f"Error on calling provider model API: " f"{response_json}",
                    )
                if response_json["model"] != provider_model_id:
                    raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"Provider model id error.")
                return TextEmbeddingResult(
                    data=[
                        TextEmbeddingOutput(embedding=output["embedding"], index=output["index"])
                        for output in response_json["data"]
                    ],
                )
