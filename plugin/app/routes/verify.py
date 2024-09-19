from fastapi import APIRouter
from typing import Any
from pydantic import BaseModel, Field, model_validator
from app.cache import get_bundle_handler
from app.error import raise_http_error, ErrorCode, TKHttpException
from app.models import validate_bundle_credentials, BundleCredentials, BundleHandler, BaseSuccessDataResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


class VerifyCredentialsRequest(BaseModel):

    bundle_id: str = Field(..., min_length=1, max_length=50)
    credentials: BundleCredentials = Field(..., description="The credentials of the model provider.")

    @model_validator(mode="before")
    def validate_before(cls, data: Any):

        # validate bundle credentials
        credentials = validate_bundle_credentials(data)
        data["credentials"] = credentials
        data.pop("encrypted_credentials", None)

        return data


@router.post(
    "/verify_credentials",
    response_model=BaseSuccessDataResponse,
    include_in_schema=False,
)
async def api_verify_credentials(
    data: VerifyCredentialsRequest,
):
    # encryption
    bundle_handler: BundleHandler = get_bundle_handler(data.bundle_id)
    if not bundle_handler:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, f"Bundle {data.bundle_id} not found.")
    try:
        await bundle_handler.verify(data.credentials)

    except TKHttpException as e:
        if isinstance(getattr(e, "detail"), dict):
            message = e.detail.get("message")
            if message:
                message = " " + message
            e.detail["message"] = f"Plugin credentials validation failed.{message}"
        raise e

    except Exception as e:
        raise_http_error(
            ErrorCode.CREDENTIALS_VALIDATION_ERROR,
            message="Plugin credentials validation failed, please check if your credentials are correct.",
        )

    data.credentials.encrypt()
    return BaseSuccessDataResponse(
        data={
            "encrypted_credentials": data.credentials.credentials,
        }
    )
