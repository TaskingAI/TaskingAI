import json
import logging
import os
from typing import Optional
from fastapi import HTTPException
from tkhelper.error import raise_http_error, ErrorCode, raise_request_validation_error

from app.models import RecordType, UploadFilePurpose
from app.config import CONFIG
from app.database import boto3_client

from .pdf import PdfFileContentLoader
from .web import WebContentLoader
from .docx import DocxFileContentLoader
from .txt import TxtContentLoader
from .html import HtmlFileContentLoader
from .markdown import MarkdownFileContentLoader

__all__ = ["load_db_content", "load_content_to_split"]

logger = logging.getLogger(__name__)

__pdf_reader = PdfFileContentLoader()
__docx_reader = DocxFileContentLoader()
__txt_reader = TxtContentLoader()
__html_reader = HtmlFileContentLoader()
__markdown_reader = MarkdownFileContentLoader()
__web_reader = WebContentLoader()

_bucket_name = CONFIG.S3_BUCKET_NAME


async def download_record_file(project_id: str, file_id: str) -> str:
    """
    Download record file from minio
    :param project_id: the project id
    :param file_id: the file id
    :return: the local file path
    """
    file_url = boto3_client.get_file_url(_bucket_name, UploadFilePurpose.RECORD_FILE.value, file_id, project_id)
    file_name = file_url.split("/")[-1]

    file_dir = CONFIG.PATH_TO_VOLUME + "/tmp/record_file"
    local_file_path = file_dir + f"/{file_name}"

    # download file
    await boto3_client.download_file_to_path(
        bucket_name=_bucket_name,
        purpose=UploadFilePurpose.RECORD_FILE.value,
        file_id=file_id,
        file_path=local_file_path,
        tenant_id=project_id,
    )

    logger.debug(f"Downloaded record file: {file_id} to {local_file_path}")

    return local_file_path


def remove_record_file(local_file_path):
    """
    Remove record file
    :param local_file_path: the local file path
    """
    if os.path.exists(local_file_path):
        os.remove(local_file_path)
        logger.debug(f"Removed record file: {local_file_path}")


async def load_db_content(
    record_type: RecordType,
    content: Optional[str],
    file_id: Optional[str],
    url: Optional[str],
) -> str:
    if record_type == RecordType.TEXT:
        processed_content = content.strip() if content else None
        if not processed_content:
            raise_request_validation_error(f"The content is empty")
        return processed_content

    elif record_type == RecordType.FILE:
        metadata = await boto3_client.get_file_metadata(
            _bucket_name, UploadFilePurpose.RECORD_FILE.value, file_id, CONFIG.PROJECT_ID
        )
        db_content = json.dumps(
            {
                "file_id": file_id,
                "file_name": metadata.get("original_file_name", ""),
                "file_size": int(metadata.get("file_size", 0)),
            }
        )
        return db_content

    elif record_type == RecordType.WEB:
        db_content = json.dumps(
            {
                "url": url,
            }
        )
        return db_content


async def load_content_to_split(
    record_type: RecordType,
    content: Optional[str],
    file_id: Optional[str],
    url: Optional[str],
) -> str:
    """
    Load content from record
    :param record_type: the record type
    :param content: the record content
    :param file_id: the file id, it is required for file record
    :return: Tuple[the content string to be saved to db, the processed content string]
    """

    if record_type == RecordType.TEXT:
        processed_content = content.strip() if content else None
        if not processed_content:
            raise_request_validation_error(f"The content is empty")
        return processed_content

    elif record_type == RecordType.FILE:
        if not file_id:
            raise_request_validation_error("file_id is required for file record")

        local_file_path = None

        try:
            local_file_path = await download_record_file(CONFIG.PROJECT_ID, file_id)
            ext = file_id.split("_")[0]

            processed_content = None
            if ext == "pdf":
                processed_content = await __pdf_reader.read_content(local_file_path)
            elif ext == "docx":
                processed_content = await __docx_reader.read_content(local_file_path)
            elif ext == "txt":
                processed_content = await __txt_reader.read_content(local_file_path)
            elif ext == "html":
                processed_content = await __html_reader.read_content(local_file_path)
            elif ext == "md":
                processed_content = await __markdown_reader.read_content(local_file_path)
            else:
                raise_request_validation_error(f"Unsupported file type: {ext}")

            if processed_content is None:
                raise_request_validation_error(f"Failed to load content from file")

            processed_content = processed_content.strip()
            if not processed_content:
                raise_request_validation_error(f"File content is empty")

            return processed_content

        except HTTPException as e:
            raise e

        except Exception as e:
            logger.error(f"Failed to load content from file {file_id}: {e}")
            raise_http_error(ErrorCode.INVALID_REQUEST, f"Failed to load content from file.")

        finally:
            if local_file_path:
                # delete from minio
                await boto3_client.delete_file(
                    _bucket_name, UploadFilePurpose.RECORD_FILE.value, file_id, CONFIG.PROJECT_ID
                )
                remove_record_file(local_file_path)

    elif record_type == RecordType.WEB:
        if not url:
            raise_request_validation_error("url is required for web record")

        if not url.startswith("https://"):
            raise_request_validation_error("Web URL must be https://")
        elif url.startswith("http://"):
            raise_request_validation_error("HTTPS is required for web URL")

        loaded_content = None

        try:
            loaded_content = await __web_reader.read_content(url)
            loaded_content = loaded_content.strip()
            logger.debug(f"loaded_content: type=web, content={loaded_content}")
        except HTTPException as e:
            logger.error(f"Failed to load content from web {url}: HTTPException {e}")
            raise e
        except Exception as e:
            logger.error(f"Failed to load content from web {url}: Exception {e}")
            raise_http_error(ErrorCode.INTERNAL_SERVER_ERROR, f"Failed to process web url {url}")

        if not loaded_content:
            raise_http_error(ErrorCode.INVALID_REQUEST, f"The web content is empty")

        return loaded_content
