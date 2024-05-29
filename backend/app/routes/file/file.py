from fastapi import APIRouter, Depends, Form, UploadFile
from fastapi import File as FastAPIFile

from app.config import CONFIG
from app.database import boto3_client
from app.models import UploadFilePurpose
from app.routes.file.utils import check_ext, check_file_size, file_purpose_dict
from app.schemas.file import UploadFileResponse
from tkhelper.error import ErrorCode, raise_http_error
from tkhelper.utils import generate_random_id

from ..utils import auth_info_required

router = APIRouter()


@router.post(
    "/files",
    tags=["File"],
    response_model=UploadFileResponse,
)
async def api_upload_file(
    purpose: UploadFilePurpose = Form(...),
    file: UploadFile = FastAPIFile(...),
    auth_info: dict = Depends(auth_info_required),
):
    purpose_info = file_purpose_dict.get(purpose)
    ext = check_ext(purpose_info, file.filename.split(".")[-1].lower())

    file_size_limit_mb = 15
    check_file_size(file_size_limit_mb, file.size)

    random_id = generate_random_id(20)
    file_id = f"{ext}_{purpose_info.id_prefix}{random_id}"

    content_bytes = await file.read()
    save_succeeded = await boto3_client.upload_file_from_bytes(
        bucket_name=CONFIG.S3_BUCKET_NAME,
        purpose=purpose.value,
        file_id=file_id,
        content_bytes=content_bytes,
        original_file_name=file.filename,
        tenant_id=CONFIG.PROJECT_ID,
    )

    if not save_succeeded:
        raise_http_error(ErrorCode.INTERNAL_SERVER_ERROR, "Failed to upload file, reason=4")

    return UploadFileResponse(data={"file_id": file_id})
