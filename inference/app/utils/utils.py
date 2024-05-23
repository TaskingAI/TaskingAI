import time
from app.error import ErrorCode, raise_http_error
import json
import hashlib
import re
from typing import List

__all__ = [
    "get_current_timestamp_int",
    "checksum",
    "is_valid_data_uri",
    "check_valid_list_content",
    "split_url",
    "build_url",
]


def get_current_timestamp_int():
    return int(time.time() * 1000)


def checksum(data) -> str:
    """
    Returns the SHA256 checksum of the given data.

    :param data: The data to checksum.
    :return: The SHA256 checksum of the given data.
    """
    data_str = json.dumps(data, sort_keys=True)
    hash_object = hashlib.sha256()
    hash_object.update(data_str.encode())
    return hash_object.hexdigest()


def is_valid_data_uri(uri: str) -> bool:
    pattern = r"^data:image\/(jpg|png|jpeg);base64,([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$"
    match = re.match(pattern, uri)
    return match is not None


def check_valid_list_content(content: List):
    for c in content:
        if c.type == "image_url":
            if not is_valid_data_uri(c.image_url.url):
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message="Invalid image URL. Only jpg, jpeg, "
                    "and png in base64 format with proper prefix "
                    "are supported.",
                )


def split_url(url: str) -> tuple:
    format_and_encoding = url[len("data:image/") :].split(";base64,")
    if len(format_and_encoding) == 2:
        image_format = format_and_encoding[0]
        encoding_content = format_and_encoding[1]
        return image_format, encoding_content
    else:
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            message="Prefix error. The url prefix should be like: 'data:image/xxx;base64,'.",
        )


def build_url(base_url, path):
    try:
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        if not path.startswith("/"):
            path = "/" + path
        return base_url + path
    except Exception as e:
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            message=f"Failed to build url: {e}",
        )
