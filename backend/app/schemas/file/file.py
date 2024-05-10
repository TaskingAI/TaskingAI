from pydantic import BaseModel, Field

from app.models.file.file import FileIdData

__all__ = ["UploadFileResponse"]


class UploadFileResponse(BaseModel):
    status: str = Field(
        "success", Literal="success", description="The status of the response."
    )
    data: FileIdData = Field(
        ...,
        description="The file API response data.",
        examples=[{"file_id": "pdf_123"}],
    )
