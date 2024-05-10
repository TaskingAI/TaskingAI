from tkhelper.error import raise_http_error, ErrorCode
from typing import List

__all__ = ["clean_pages_content"]


def clean_pages_content(pages: List[str]):
    cleaned_pages = []
    for page in pages:
        cleaned_content = page.replace("\x00", "")
        cleaned_pages.append(cleaned_content)

    content = "\n\n".join(cleaned_pages).strip()
    if not content:
        raise_http_error(
            ErrorCode.INVALID_REQUEST,
            "There is no textual content in the file.",
        )
    return content
