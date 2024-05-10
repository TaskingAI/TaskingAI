from enum import Enum

from pydantic import BaseModel, Field

__all__ = ["ImageData", "UploadImagePurpose"]


class ImageData(BaseModel):
    url: str = Field(..., description="The image url.")


class UploadImagePurpose(str, Enum):
    USER_MESSAGE_IMAGE = "user_message_image"
