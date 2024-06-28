from fastapi import APIRouter
from app.models import (
    validate_credentials,
    validate_model_info,
    ModelType,
)
from app.cache import get_rerank_model
from app.error import raise_http_error, ErrorCode, TKHttpException, error_messages
from app.models.tokenizer import string_tokens
from app.models.rerank import *
from .schema import *
from config import CONFIG
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/rerank",
    operation_id="rerank",
    summary="Rerank",
    tags=["Inference"],
    responses={422: {"description": "Unprocessable Entity"}},
    response_model=RerankResponse,
)
async def api_rerank(
    data: RerankRequest,
):
    # validate model info
    model_infos = [
        validate_model_info(
            model_schema_id=data.model_schema_id,
            provider_model_id=data.provider_model_id,
            properties_dict={},
            model_type=ModelType.RERANK,
        )
    ]

    # validate credentials
    provider_credentials = validate_credentials(
        model_infos=model_infos,
        credentials_dict=data.credentials,
        encrypted_credentials_dict=data.encrypted_credentials,
    )

    for model_info in model_infos:
        model_type = model_info[3]
        if model_type != ModelType.RERANK and model_type != ModelType.WILDCARD:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Model type should be rerank, but got " + model_type)

    (model_schema, provider_model_id, properties, _) = model_infos[0]

    # check if proxy is blacklisted
    if data.proxy:
        for url in CONFIG.PROVIDER_URL_BLACK_LIST:
            if url in data.proxy:
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"Invalid provider url: {url}")

    try:
        model = get_rerank_model(provider_id=model_schema.provider_id)
        if not model:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR,
                f"Provider {model_schema.provider_id} is not " f"supported through the rerank API.",
            )
        tokens = string_tokens(data.query)
        for d in data.documents:
            tokens += string_tokens(d)

        result = await model.rerank(
            provider_model_id=provider_model_id,
            credentials=provider_credentials,
            query=data.query,
            documents=data.documents,
            top_n=data.top_n,
            proxy=data.proxy,
            custom_headers=data.custom_headers,
        )
        for r in result.results:
            tokens += string_tokens(r.document.text) + 1
        usage = RerankUsage(
            input_tokens=tokens,
            output_tokens=tokens,
        )
        return RerankResponse(data=result, usage=usage)
    except TKHttpException as e:
        logger.error(f"rerank: provider {model_schema.provider_id} error = {e}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled exception for provider {model_schema.provider_id}: {str(e)}")
        raise TKHttpException(
            status_code=error_messages[ErrorCode.INTERNAL_SERVER_ERROR]["status_code"],
            detail={"error_code": ErrorCode.INTERNAL_SERVER_ERROR, "message": str(e)},
        )
