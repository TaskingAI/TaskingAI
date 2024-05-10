from enum import Enum

from pydantic import BaseModel, Field

__all__ = ["FileIdData", "UploadFilePurpose"]


class FileIdData(BaseModel):
    file_id: str = Field(..., description="The file id.")


class UploadFilePurpose(str, Enum):
    RECORD_FILE = "record_file"
