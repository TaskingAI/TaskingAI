from starlette.responses import FileResponse

from fastapi import APIRouter, Request
from app.error import ErrorCode, raise_http_error
import os
from app.cache import get_provider

router = APIRouter()


@router.get(
    "/providers/icons/{provider_id}.svg",
    tags=["Model"],
    summary="Get Provider Icon File",
    operation_id="get_provider_icon",
    responses={422: {"description": "Unprocessable Entity"}},
)
async def api_get_provider_icon(provider_id: str, request: Request):
    provider = get_provider(provider_id)
    if not provider:
        raise_http_error(
            ErrorCode.OBJECT_NOT_FOUND,
            message=f"Provider {provider_id} not found.",
        )

    current_path = os.path.dirname(os.path.abspath(__file__))
    svg_file_path = f"../../../providers/{provider_id}/resources/icon.svg"
    abs_svg_file_path = os.path.join(current_path, svg_file_path)

    return FileResponse(
        path=abs_svg_file_path,
        headers={"Content-Disposition": "inline"},
        media_type="image/svg+xml",
        filename=f"{provider_id}.svg",
    )
