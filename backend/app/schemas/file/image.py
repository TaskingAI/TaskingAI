from pydantic import BaseModel, Field

from app.models.file import ImageData

__all__ = ["UploadImageResponse"]


class UploadImageResponse(BaseModel):
    status: str = Field(
        "success", Literal="success", description="The status of the response."
    )
    data: ImageData = Field(
        ...,
        description="The image data.",
        examples=[{"image": "https://tasking.ai/image.png"}],
    )
