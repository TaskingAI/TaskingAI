from app.schemas.model import TextEmbeddingRequest, TextEmbeddingResponse
from app.routes.openai.schemas import (
    OpenaiTextEmbeddingRequest,
    OpenaiTextEmbeddingResponse,
    OpenaiEmbeddingUsage,
    OpenaiEmbedding,
)
from tkhelper.error import raise_request_validation_error


def adapt_openai_text_embedding_input(data: OpenaiTextEmbeddingRequest) -> TextEmbeddingRequest:
    model_id = data.model

    if isinstance(data.input, str):
        input_data = data.input
    elif isinstance(data.input, list) and all(isinstance(item, str) for item in data.input):
        input_data = data.input
    else:
        raise_request_validation_error("input must be a string or a list of strings.")

    # Construct the new TextEmbeddingRequest
    return TextEmbeddingRequest(model_id=model_id, input=input_data, input_type=None)


def adapt_openai_text_embedding_response(
    response: TextEmbeddingResponse, data: OpenaiTextEmbeddingRequest
) -> OpenaiTextEmbeddingResponse:
    openai_embeddings = [
        OpenaiEmbedding(embedding=embedding.embedding, index=embedding.index, object="embedding")
        for embedding in response.data
    ]

    # Extract the model used from the original request to OpenAI as it's not part of the TextEmbeddingResponse.
    model_used = data.model

    # Map the usage data directly since both usages are expected to be compatible or have the same format.
    # If there are differences in format, appropriate conversions or mappings need to be applied.
    openai_usage = OpenaiEmbeddingUsage(
        prompt_tokens=response.usage.input_tokens, total_tokens=response.usage.input_tokens
    )

    # Construct the new OpenaiTextEmbeddingResponse using the mapped data.
    return OpenaiTextEmbeddingResponse(
        data=openai_embeddings,
        model=model_used,
        object="list",  # This is always 'list' as specified.
        usage=openai_usage,
    )
