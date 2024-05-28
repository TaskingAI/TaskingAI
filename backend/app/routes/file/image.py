from fastapi import APIRouter, Depends, Form, UploadFile
from fastapi import File as FastAPIFile

from app.config import CONFIG
from app.database import boto3_client
from app.models import UploadImagePurpose
from app.routes.file.utils import image_purpose_dict
from app.routes.utils import auth_info_required
from app.schemas import UploadImageResponse
from tkhelper.error import ErrorCode, raise_http_error, raise_request_validation_error
from tkhelper.utils import generate_random_id

router = APIRouter()


@router.post(
    "/images",
    tags=["File"],
    response_model=UploadImageResponse,
)
async def upload_image(
    purpose: UploadImagePurpose = Form(...),
    image: UploadFile = FastAPIFile(...),
    auth_info: dict = Depends(auth_info_required),
):
    ext = image.filename.split(".")[-1].lower()

    purpose_info = image_purpose_dict.get(purpose)

    image_size_limit_mb = 5

    if image.size > image_size_limit_mb * 1024 * 1024:
        raise_request_validation_error("image size is too large.")

    if ext not in purpose_info.allow_file_formats:
        raise_request_validation_error(
            f"File format is not supported, supported formats: {', '.join(purpose_info.allow_file_formats.keys())}"
        )
    ext = purpose_info.allow_file_formats[ext]

    random_id = generate_random_id(20)
    file_id = f"{ext}_{purpose_info.id_prefix}{random_id}"

    content_bytes = await image.read()
    image_url = await boto3_client.upload_file_from_bytes(
        bucket_name=CONFIG.S3_BUCKET_NAME,
        purpose=purpose.value,
        file_id=file_id,
        content_bytes=content_bytes,
        original_file_name=image.filename,
        tenant_id=CONFIG.PROJECT_ID,
        return_url=True,
    )

    if not image_url:
        raise_http_error(ErrorCode.INTERNAL_SERVER_ERROR, "Failed to upload image.")

    return UploadImageResponse(data={"url": image_url})
