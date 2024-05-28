from fastapi import APIRouter, Depends, Request
from typing import Dict

from app.models import Model
from app.services.model.model import get_model

from app.schemas.model import TextEmbeddingRequest, TextEmbeddingResponse
from app.services.inference.text_embedding import text_embedding
from .schemas import OpenaiTextEmbeddingRequest
from ..utils import auth_info_required, check_http_error

from .utils import (
    adapt_openai_text_embedding_input,
    adapt_openai_text_embedding_response,
)

router = APIRouter()


# add new add_api_key
@router.post(
    "/embeddings",
    summary="Text Embedding",
    operation_id="text_embedding",
    tags=["Inference"],
    responses={422: {"description": "Unprocessable Entity"}},
    description="Model inference for text embedding.",
)
async def api_text_embedding_openai(
    request: Request,
    openai_data: OpenaiTextEmbeddingRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    data: TextEmbeddingRequest = adapt_openai_text_embedding_input(openai_data)
    # validate model
    model: Model = await get_model(
        model_id=data.model_id,
    )

    response = await text_embedding(
        model=model,
        encrypted_credentials=model.encrypted_credentials,
        input_text_list=data.input,
        input_type=data.input_type,
    )
    check_http_error(response)
    response = TextEmbeddingResponse(
        status="success", data=response._json_data["data"], usage=response._json_data["usage"]
    )

    openai_response = adapt_openai_text_embedding_response(response, openai_data)
    openai_response_dict = openai_response.model_dump()
    return openai_response_dict
