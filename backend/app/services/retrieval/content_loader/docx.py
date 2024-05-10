from tkhelper.error import raise_http_error, ErrorCode
from docx import Document
from docx.opc.exceptions import PackageNotFoundError
import os
import logging

from .base import BaseFileLoader
from .utils import clean_pages_content

logger = logging.getLogger(__name__)


class DocxFileContentLoader(BaseFileLoader):
    async def read_content(self, path):
        # Check if the file exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file {path} does not exist.")

        try:
            document = Document(path)
            result = [paragraph.text for paragraph in document.paragraphs]

            # Process each page and remove null bytes
            result = clean_pages_content(result)
            return result

        except PackageNotFoundError:
            # Handle cases where the file does not seem to be a valid docx
            raise_http_error(ErrorCode.INVALID_REQUEST, "The file is not a valid docx file.")
        except Exception as e:
            # General exception for any other unexpected errors
            logger.error(f"An error occurred while reading the file {path}: {e}")
            raise_http_error(ErrorCode.INVALID_REQUEST, "Failed to load textual content from the docx file.")
