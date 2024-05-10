from tkhelper.error import raise_http_error, ErrorCode
from fastapi import HTTPException
from langchain_community.document_loaders import PyPDFLoader
import logging

from .base import BaseFileLoader
from .utils import clean_pages_content

logger = logging.getLogger(__name__)


class PdfFileContentLoader(BaseFileLoader):
    async def read_content(self, path):
        try:
            pdf_loader = PyPDFLoader(path)
            data = pdf_loader.load()

            # Process each page and remove null bytes
            pages = [page.page_content for page in data]
            result = clean_pages_content(pages)
            return result

        except HTTPException as e:
            raise e

        except Exception as e:
            # Log the exception or handle it accordingly
            logger.error(f"Failed to load PDF content: {e}")
            raise_http_error(ErrorCode.INVALID_REQUEST, "Failed to load PDF content due to encoding error.")
