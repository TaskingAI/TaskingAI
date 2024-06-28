from fastapi import APIRouter
from app.models import (
    ProviderCredentials,
    validate_credentials,
    validate_model_info,
    ModelType,
)
from app.cache import get_text_embedding_model
from app.error import raise_http_error, ErrorCode, TKHttpException, error_messages
from app.models.tokenizer import string_tokens
import asyncio
from .schema import *
import logging
from typing import List, Optional
import numpy as np
from config import CONFIG

logger = logging.getLogger(__name__)

router = APIRouter()


async def embed_batch(
    model: BaseTextEmbeddingModel,
    provider_model_id: str,
    batch_input: List[str],
    credentials: ProviderCredentials,
    configs: TextEmbeddingModelConfiguration,
    input_type: Optional[TextEmbeddingInputType] = None,
    proxy: Optional[str] = None,
    custom_headers: Optional[Dict[str, str]] = None,
):
    # Embed a single batch of texts
    res = await model.embed_text(
        provider_model_id=provider_model_id,
        input=batch_input,
        credentials=credentials,
        configs=configs,
        input_type=input_type,
        proxy=proxy,
        custom_headers=custom_headers,
    )
    # ensure that the embeddings are unit vectors
    embeddings_array = np.array([output.embedding for output in res.data])

    try:
        norms = np.linalg.norm(embeddings_array, axis=1, keepdims=True)
        not_unit_vectors = (norms > 0).flatten()
        embeddings_array[not_unit_vectors] = embeddings_array[not_unit_vectors] / norms.flatten()[
            not_unit_vectors
        ].reshape(-1, 1)
    except Exception as e:
        logging.exception("Failed to normalize embeddings: %s", e)
        raise

    for i, output in enumerate(res.data):
        output.embedding = embeddings_array[i].tolist()

    return res


async def embed_text(
    provider_id: str,
    provider_model_id: str,
    input: List[str],
    credentials: ProviderCredentials,
    properties: TextEmbeddingModelProperties,
    configs: TextEmbeddingModelConfiguration,
    input_type: Optional[TextEmbeddingInputType] = None,
    proxy: Optional[str] = None,
    custom_headers: Optional[Dict[str, str]] = None,
) -> TextEmbeddingResult:
    model = get_text_embedding_model(provider_id=provider_id)
    batch_size = properties.max_batch_size if properties else 512

    if not model:
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            f"Provider {provider_id} is not " f"supported through the text_embedding API.",
        )
    # Split input into batches
    batches = [input[i : i + batch_size] for i in range(0, len(input), batch_size)]

    merged_results = []  # Initialize merged results list

    # Process in chunks of 20 to respect max parallel tasks limit
    max_parallel_tasks = 20
    for i in range(0, len(batches), max_parallel_tasks):
        tasks = []
        for batch in batches[i : i + max_parallel_tasks]:
            task = embed_batch(
                model=model,
                provider_model_id=provider_model_id,
                batch_input=batch,
                credentials=credentials,
                configs=configs,
                input_type=input_type,
                proxy=proxy,
                custom_headers=custom_headers,
            )
            tasks.append(task)

        # Run embedding in parallel for each batch within the current chunk
        batch_results = await asyncio.gather(*tasks)

        # Merge results while maintaining order
        for batch_result in batch_results:
            merged_results.extend(batch_result.data)
    usage = TextEmbeddingUsage(input_tokens=sum(string_tokens(i) for i in input))
    return TextEmbeddingResult(data=merged_results, usage=usage)


# Note: TextEmbeddingResult should be structured to accumulate and return results from multiple batches.


# add new add_api_key
@router.post(
    "/text_embedding",
    operation_id="text_embedding",
    summary="Text Embedding",
    tags=["Inference"],
    responses={422: {"description": "Unprocessable Entity"}},
    response_model=TextEmbeddingResponse,
)
async def api_text_embedding(
    data: TextEmbeddingRequest,
):
    # validate model info
    model_infos = [
        validate_model_info(
            model_schema_id=data.model_schema_id,
            provider_model_id=data.provider_model_id,
            properties_dict=data.properties,
            model_type=ModelType.TEXT_EMBEDDING,
        )
    ]
    # validate fallback model info
    if data.fallbacks:
        for fallback in data.fallbacks:
            model_infos.append(
                validate_model_info(
                    model_schema_id=fallback.model_schema_id,
                    provider_model_id=fallback.provider_model_id,
                    properties_dict=data.properties,
                    model_type=ModelType.TEXT_EMBEDDING,
                )
            )

    # validate credentials
    provider_credentials = validate_credentials(
        model_infos=model_infos,
        credentials_dict=data.credentials,
        encrypted_credentials_dict=data.encrypted_credentials,
    )

    for model_info in model_infos:
        model_type = model_info[3]
        if model_type != ModelType.TEXT_EMBEDDING and model_type != ModelType.WILDCARD:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR, "Model type should be text_embedding, but got " + model_type
            )

    input = data.input
    if isinstance(data.input, str):
        input = [data.input]

    default_embedding_size = model_infos[0][2].embedding_size
    last_exception = None

    # check if proxy is blacklisted
    if data.proxy:
        for url in CONFIG.PROVIDER_URL_BLACK_LIST:
            if url in data.proxy:
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"Invalid provider url: {url}")

    for i, (model_schema, provider_model_id, properties, _) in enumerate(model_infos):
        properties: TextEmbeddingModelProperties
        if default_embedding_size != properties.embedding_size:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR,
                "The embedding size of the fallback model '{}': {} is different from the primary model '{}': {}.".format(
                    provider_model_id, properties.embedding_size, model_infos[0][1], default_embedding_size
                ),
            )
        try:
            response = await embed_text(
                provider_id=model_schema.provider_id,
                provider_model_id=provider_model_id,
                input=input,
                credentials=provider_credentials,
                properties=properties,
                configs=data.configs,
                input_type=data.input_type,
                proxy=data.proxy,
                custom_headers=data.custom_headers,
            )
            fallback_index = None
            if i:
                fallback_index = i - 1
            return TextEmbeddingResponse(data=response.data, usage=response.usage, fallback_index=fallback_index)
        except TKHttpException as e:
            logger.error(f"text_embedding: provider {model_schema.provider_id} error = {e}")
            last_exception = e
        except Exception as e:
            logger.error(f"Unhandled exception for provider {model_schema.provider_id}: {str(e)}")
            last_exception = TKHttpException(
                status_code=error_messages[ErrorCode.INTERNAL_SERVER_ERROR]["status_code"],
                detail={"error_code": ErrorCode.INTERNAL_SERVER_ERROR, "message": str(e)},
            )
    if last_exception:
        raise last_exception  # Raise the last caught exception if all models fail

    # TODO: raise_http_error(ErrorCode.PROVIDER_SERVICE_UNAVAILABLE, "All providers' service are unavailable")
