from starlette.responses import FileResponse

from fastapi import APIRouter, Request
from app.error import ErrorCode, raise_http_error
import os
from app.cache import get_bundle

router = APIRouter()


@router.get(
    "/plugins/bundles/icons/{bundle_id}.png",
    tags=["Plugin"],
    summary="Get bundle Icon File",
    operation_id="get_bundle_icon",
    responses={422: {"description": "Unprocessable Entity"}},
)
async def api_get_bundle_icon(
        bundle_id: str,
        request: Request,
):
    bundle = get_bundle(bundle_id)
    if not bundle:
        raise_http_error(
            ErrorCode.OBJECT_NOT_FOUND,
            message=f"bundle {bundle_id} not found.",
        )

    current_path = os.path.dirname(os.path.abspath(__file__))
    png_file_path = f"../../bundles/{bundle_id}/resources/icon.png"
    abs_png_file_path = os.path.join(current_path, png_file_path)

    return FileResponse(
        path=abs_png_file_path,
        headers={"Content-Disposition": "inline"},
        media_type="image/png",
        filename=f"{bundle_id}.png",
    )
