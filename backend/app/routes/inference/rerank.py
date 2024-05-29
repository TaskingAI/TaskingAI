from fastapi import APIRouter, Depends, Request
from typing import Dict
from ..utils import auth_info_required
from tkhelper.utils import check_http_error
from app.schemas.model.rerank import RerankRequest, RerankResponse
from app.models.inference.rerank import RerankResult
from app.services.inference.rerank import rerank
from app.services.model.model import get_model
from app.models import Model

router = APIRouter()


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
    model: Model = await get_model(
        model_id=data.model_id,
    )

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
