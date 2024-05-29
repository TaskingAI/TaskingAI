from provider_dependency.text_embedding import *
from aiobotocore.session import get_session
from typing import List, Dict, Optional

cohere_input_type_map = {
    TextEmbeddingInputType.document: "search_document",
    TextEmbeddingInputType.query: "search_query",
}


class AwsBedrockTextEmbeddingModel(BaseTextEmbeddingModel):
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
        model_prefix = provider_model_id.split(".")[0]
        payload = {}
        if model_prefix == "cohere":
            if input_type is None:
                input_type = TextEmbeddingInputType.document
            cohere_input_type = cohere_input_type_map[input_type]

            payload = {
                "texts": input,
                "input_type": cohere_input_type,
            }

        session = get_session()
        async with session.create_client(
            service_name="bedrock-runtime",
            region_name=credentials.AWS_REGION,
            aws_access_key_id=credentials.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=credentials.AWS_SECRET_ACCESS_KEY,
        ) as runtime_client:
            try:
                body_jsonstr = json.dumps(payload)
                response = await runtime_client.invoke_model(
                    modelId=provider_model_id, contentType="application/json", accept="*/*", body=body_jsonstr
                )
                response_content = await response["body"].read()
                result = json.loads(response_content.decode("utf-8"))
                if model_prefix == "cohere":
                    return TextEmbeddingResult(
                        data=[
                            TextEmbeddingOutput(embedding=output, index=i)
                            for i, output in enumerate(result["embeddings"])
                        ],
                    )

            except Exception as e:
                raise_http_error(ErrorCode.PROVIDER_ERROR, f"Error invoking model: {e}")
