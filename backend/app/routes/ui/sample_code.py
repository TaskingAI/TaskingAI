from typing import Dict

from fastapi import APIRouter, Depends
from starlette.requests import Request
from tkhelper.schemas import BaseDataResponse

from app.routes.utils import auth_info_required
from app.services.ui.sample_code import SampleCodeModule, get_sample_codes

router = APIRouter()


@router.get(
    "/ui/template_codes/get_code",
    tags=["Sample Code"],
    summary="Get sample code",
    response_model=BaseDataResponse,
)
async def get_code(
    request: Request,
    module: SampleCodeModule,
    auth_info: Dict = Depends(auth_info_required),
):
    return BaseDataResponse(data=get_sample_codes(module))
