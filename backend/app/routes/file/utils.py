from enum import Enum
from typing import Dict

from app.models.file import UploadFilePurpose, UploadImagePurpose
from tkhelper.error import raise_request_validation_error


class UploadFileModule(str, Enum):
    ASSISTANT = "assistant"
    RETRIEVAL = "retrieval"


class PurposeInfo:
    def __init__(
        self,
        module: UploadFileModule,
        id_prefix: str,
        service_name: str,
        policy_name: str,
        allow_file_formats: Dict[str, str],
    ):
        self.module = module
        self.id_prefix = id_prefix
        self.service_name = service_name
        self.policy_name = policy_name
        self.allow_file_formats = allow_file_formats


file_purpose_dict = {
    UploadFilePurpose.RECORD_FILE: PurposeInfo(
        UploadFileModule.RETRIEVAL,
        "Jde5",
        "retrieval",
        "record_file_size_limit_mb",
        {
            "pdf": "pdf",
            "docx": "docx",
            "md": "md",
            "txt": "txt",
            "html": "html",
            "htm": "html",
        },
    ),
}


image_purpose_dict = {
    UploadImagePurpose.USER_MESSAGE_IMAGE: PurposeInfo(
        UploadFileModule.ASSISTANT,
        "umIM",
        "assistant",
        "user_message_image_size_limit_mb",
        {"jpg": "jpg", "jpeg": "jpg", "png": "png"},
    ),
}


def check_file_size(limit_mb: int, size: int):
    if size > limit_mb * 1024 * 1024:
        raise_request_validation_error("File size is too large.")


def check_ext(purpose_info: PurposeInfo, ext: str):
    if ext not in purpose_info.allow_file_formats:
        raise_request_validation_error(
            f"File format is not supported, supported formats: {', '.join(purpose_info.allow_file_formats.keys())}"
        )
    return purpose_info.allow_file_formats[ext]
