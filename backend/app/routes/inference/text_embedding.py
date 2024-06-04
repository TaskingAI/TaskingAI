import logging
from fastapi import APIRouter, Depends, Request, HTTPException
from typing import Dict
from ..utils import auth_info_required
from tkhelper.utils import check_http_error
from tkhelper.error import raise_http_error, ErrorCode
from app.schemas.model.text_embedding import TextEmbeddingRequest, TextEmbeddingResponse
from app.services.inference.text_embedding import text_embedding
from app.services.model.model import get_model
from app.models import Model

router = APIRouter()

logger = logging.Logger(__name__)


@router.post(
    "/inference/text_embedding",
    summary="Text Embedding",
    operation_id="text_embedding",
    tags=["Inference"],
    responses={422: {"description": "Unprocessable Entity"}},
    description="Model inference for text embedding.",
    response_model=TextEmbeddingResponse,
)
async def api_text_embedding(
    request: Request,
    data: TextEmbeddingRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    # validate model
    base_model: Model = await get_model(
        model_id=data.model_id,
    )

    fallbacks = base_model.fallbacks.model_list
    models_to_attempt = [base_model.model_id] + ([fb.model_id for fb in fallbacks] if fallbacks else [])
    main_exception = None

    for i, model_id in enumerate(models_to_attempt):
        model = await get_model(model_id=model_id)
        try:
            response = await text_embedding(
                model=model,
                encrypted_credentials=model.encrypted_credentials,
                input_text_list=data.input,
                input_type=data.input_type,
            )
            check_http_error(response)
            return TextEmbeddingResponse(data=response.json()["data"], usage=response.json()["usage"])
        except HTTPException as e:
            if e.status_code == 422:
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, e.detail)
            if i == 0:
                main_exception = e.detail
            logger.debug(f"Model {model_id} failed to respond: {e.detail}")
            continue
        except Exception as e:
            raise e

    if fallbacks:
        raise_http_error(
            ErrorCode.PROVIDER_ERROR,
            f"All models failed to respond. Main model {data.model_id} error: {main_exception}",
        )
    else:
        raise_http_error(ErrorCode.PROVIDER_ERROR, f"Model {data.model_id} failed to respond: " + main_exception)
