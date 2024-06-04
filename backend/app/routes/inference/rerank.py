import logging
from fastapi import APIRouter, Depends, Request, HTTPException
from typing import Dict
from ..utils import auth_info_required
from tkhelper.utils import check_http_error
from tkhelper.error import raise_request_validation_error, raise_http_error, ErrorCode
from app.schemas.model.rerank import RerankRequest, RerankResponse
from app.models.inference.rerank import RerankResult
from app.services.inference.rerank import rerank
from app.services.model.model import get_model
from app.models import Model

router = APIRouter()

logger = logging.Logger(__name__)


@router.post(
    "/inference/rerank",
    summary="Rerank",
    operation_id="rerank",
    tags=["Inference"],
    responses={422: {"description": "Unprocessable Entity"}},
    description="Model inference for rerank.",
    response_model=RerankResponse,
)
async def api_rerank(
    request: Request,
    data: RerankRequest,
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

        if not model.is_rerank():
            raise_request_validation_error(f"Model {model.model_id} a is not rerank model.")
        try:
            # generate none stream response
            response = await rerank(
                model=model,
                encrypted_credentials=model.encrypted_credentials,
                query=data.query,
                documents=data.documents,
                top_n=data.top_n,
            )
            check_http_error(response)
            data = RerankResult(results=response.json()["data"]["results"])
            return RerankResponse(data=data, usage=response.json()["usage"])
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
