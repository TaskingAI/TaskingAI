import io
import logging
import os
from enum import Enum
from typing import Dict, Optional, Tuple

import aioboto3
import aiofiles
import aiofiles.os
from pathvalidate import sanitize_filename

from tkhelper.error import ErrorCode, raise_http_error
from tkhelper.utils import decode_base64_to_text, encode_text_to_base64, get_base62_date

logger = logging.getLogger(__name__)

image_extensions = ["jpg", "jpeg", "png"]


class StorageClientType(str, Enum):
    LOCAL = "local"
    S3 = "s3"


def _validate_file_id(file_id: str) -> Tuple[str, str]:
    """
    Validate file_id
    :param file_id: the id of the file, e.g. txt_x123456
    :return: the extension and the id
    """
    parts = file_id.split("_")
    if len(parts) != 2:
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            f"Invalid file_id: {file_id}",
        )
    return parts[0], parts[1]


def _object_key(
    purpose: str,
    file_id: str,
    ext: str,
    tenant_id: str,
    original_name: Optional[str] = None,
) -> str:
    type_path = "imgs/" if (ext in image_extensions) else "files/"
    purpose_path = f"{purpose[0]}/"
    tenant_path = f"{tenant_id}/"
    date_path = f"{get_base62_date()}/"
    ext = f"/{original_name}" if original_name else f".{ext}"

    return f"{type_path}{purpose_path}{tenant_path}{date_path}{file_id}{ext}"


class StorageClient:
    def __init__(
        self,
        service_name: StorageClientType,
        endpoint_url: Optional[str] = None,
        bucket_public_domain: Optional[str] = None,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        path_to_volume: Optional[str] = None,
        host_url: Optional[str] = None,
    ):
        if service_name == StorageClientType.S3:
            if not (endpoint_url and access_key_id and access_key_secret):
                raise ValueError("Missing S3 credentials.")
            self._session = aioboto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=access_key_secret)
        elif service_name == StorageClientType.LOCAL:
            if not path_to_volume:
                raise ValueError("Missing path to volume.")
            self._session = None
            self._volume = os.path.abspath(path_to_volume)
        else:
            raise ValueError("Invalid service name.")

        self._service_name = service_name
        self._endpoint_url = endpoint_url
        self._bucket_public_domain = bucket_public_domain
        self._host_url = host_url
        self._is_s3 = service_name == StorageClientType.S3

    async def init(self):
        logger.info("Storage client initialized.")

    async def close(self):
        logger.info("Storage client closed.")

    async def clean_data(self):
        pass

    async def health_check(self) -> bool:
        return True

    async def upload_file_from_path(
        self,
        bucket_name: str,
        purpose: str,
        file_id: str,
        file_path: str,
        tenant_id: str,
        metadata: Dict = {},
    ):
        """
        Upload file to minio
        :param bucket_name: the name of the bucket
        :param purpose: the purpose of the file
        :param file_id: the id of the file, e.g. txt_x123456
        :param file_path: the path of the file
        :param tenant_id: the id of the tenant
        :param metadata: the metadata of the file, a dict
        """

        async with aiofiles.open(file_path, "rb") as file:
            content_bytes = await file.read()
            original_file_name = (sanitize_filename(os.path.basename(file_path))).replace(" ", "_")
            await self.upload_file_from_bytes(
                bucket_name=bucket_name,
                purpose=purpose,
                file_id=file_id,
                content_bytes=content_bytes,
                original_file_name=original_file_name,
                tenant_id=tenant_id,
                metadata=metadata,
            )

    async def upload_file_from_bytes(
        self,
        bucket_name: str,
        purpose: str,
        file_id: str,
        content_bytes: bytes,
        original_file_name: str,
        tenant_id: str,
        metadata: Dict = {},
        return_url: bool = False,
    ):
        """
        Upload file to minio
        :param bucket_name: the name of the bucket
        :param purpose: the purpose of the file
        :param file_id: the id of the file, e.g. txt_x123456
        :param content_bytes: the content of the file
        :param original_file_name: the original file name
        :param tenant_id: the id of the tenant
        :param metadata: the metadata of the file, a dict
        :return: True if the file is uploaded successfully, False otherwise
        """

        metadata = metadata or {}
        original_file_name = (sanitize_filename(original_file_name)).replace(" ", "_")
        metadata["base64_file_name"] = encode_text_to_base64(original_file_name, exclude_padding=True)
        metadata["file_size"] = str(len(content_bytes))
        metadata["tenant_id"] = tenant_id

        try:
            ext, _id = _validate_file_id(file_id)
            """ upload_fileobj params
            :param Fileobj: BinaryIO
            :param Bucket: str
            :param Key: str
            :param ExtraArgs: Optional[Dict[str, Any]] = None
            :param Callback: Optional[Callable[[int], None]] = None
            :param Config: Optional[S3TransferConfig] = None    # boto3.s3.transfer.TransferConfig
            :param Processing: Callable[[bytes], bytes] = None
            """
            if self._is_s3:
                key = _object_key(purpose, _id, ext, tenant_id)
                async with self._session.client(
                    service_name=self._service_name, endpoint_url=self._endpoint_url
                ) as client:
                    await client.upload_fileobj(
                        Fileobj=io.BytesIO(content_bytes),
                        Bucket=bucket_name,
                        Key=key,
                        ExtraArgs={"Metadata": metadata or {}},
                    )
                if return_url:
                    domain = self._bucket_public_domain or f"{self._endpoint_url}/{bucket_name}"
                    return f"{domain}/{key}"
            else:
                key = _object_key(purpose, _id, ext, tenant_id, original_file_name)
                await self.save_to_volume(file_bytes=content_bytes, path=key)
                if return_url:
                    return f"{self._host_url}/{key}"
            return True
        except Exception as e:
            logger.debug(f"upload_file_from_bytes: failed to upload file {file_id}, e={e}")
            return False

    async def check_file_exists(
        self,
        bucket_name: str,
        purpose: str,
        file_id: str,
        tenant_id: str,
    ) -> bool:
        """
        Check if file exists in minio
        :param bucket_name: the name of the bucket
        :param purpose: the purpose of the file
        :param file_id: the id of the file
        :param tenant_id: the id of the tenant. Error will be raised if the tenant_id is not valid
        :return: the metadata of the file, a dict
        """

        # check if metadata exists
        try:
            ext, _id = _validate_file_id(file_id)
            key = _object_key(purpose, _id, ext, tenant_id)
            if self._is_s3:
                async with self._session.client(
                    service_name=self._service_name, endpoint_url=self._endpoint_url
                ) as client:
                    await client.head_object(
                        Bucket=bucket_name,
                        Key=key,
                    )
            else:
                path = key.removesuffix(f".{ext}")
                await self.check_volume_file_exists(path=path)

            return True
        except Exception as e:
            logger.debug(f"check_file_exists: failed to check file {file_id}, e={e}")
            return False

    async def get_file_metadata(
        self,
        bucket_name: str,
        purpose: str,
        file_id: str,
        tenant_id: str,
    ) -> Dict:
        """
        Get metadata from minio
        :param bucket_name: the name of the bucket
        :param purpose: the purpose of the file
        :param file_id: the id of the file
        :param tenant_id: the id of the tenant. Error will be raised if the tenant_id is not valid
        :return: the metadata of the file, a dict
        """

        ext, _id = _validate_file_id(file_id)
        key = _object_key(purpose, _id, ext, tenant_id)
        try:
            if self._is_s3:
                async with self._session.client(
                    service_name=self._service_name, endpoint_url=self._endpoint_url
                ) as client:
                    response = await client.head_object(
                        Bucket=bucket_name,
                        Key=key,
                    )
                file_metadata = response["Metadata"]
                base64_name = file_metadata.pop("base64_file_name", None)
                if base64_name:
                    file_metadata["original_file_name"] = decode_base64_to_text(base64_name)
                return file_metadata

            path = key.removesuffix(f".{ext}")
            return await self.get_volume_file_metadata(path=path)
        except Exception as e:
            logger.debug(f"get_file_metadata: failed to get file {file_id}, e={e}")
            raise_http_error(ErrorCode.OBJECT_NOT_FOUND, f"File {file_id} not found")

    async def download_file_to_bytes(self, bucket_name: str, purpose: str, file_id: str, tenant_id: str) -> bytes:
        """
        Download file from minio
        :param bucket_name: the name of the bucket
        :param purpose: the purpose of the file
        :param file_id: the id of the file, e.g. txt_x123456
        :param tenant_id: the id of the tenant. Error will be raised if the tenant_id is not valid
        """

        ext, _id = _validate_file_id(file_id)
        key = _object_key(purpose, _id, ext, tenant_id)
        try:
            if self._is_s3:
                async with self._session.client(
                    service_name=self._service_name, endpoint_url=self._endpoint_url
                ) as client:
                    response = await client.get_object(
                        Bucket=bucket_name,
                        Key=key,
                    )
                data = await response["Body"].read()
                logger.debug(f"download_file_to_bytes: downloaded Minio file to bytes: {_id}.{ext}")
                return data

            path = key.removesuffix(f".{ext}")
            return await self.read_volume_file(path=path)
        except Exception:
            logger.debug(f"download_file_to_bytes: failed to download file {file_id}")
            raise_http_error(ErrorCode.OBJECT_NOT_FOUND, "Failed to download file")

    async def download_file_to_path(
        self,
        bucket_name: str,
        purpose: str,
        file_id: str,
        file_path: str,
        tenant_id: str,
    ) -> bool:
        """
        Download file from minio
        :param bucket_name: the name of the bucket
        :param purpose: the purpose of the file
        :param file_id: the id of the file, e.g. txt_x123456
        :param file_path: the path of the file
        :param tenant_id: the id of the tenant. Error will be raised if the tenant_id is not valid
        :return: True if the file is downloaded successfully, False otherwise
        """
        ext, _id = _validate_file_id(file_id)
        key = _object_key(purpose, _id, ext, tenant_id)
        # download file
        try:
            if self._is_s3:
                async with self._session.client(
                    service_name=self._service_name, endpoint_url=self._endpoint_url
                ) as client:
                    response = await client.get_object(
                        Bucket=bucket_name,
                        Key=key,
                    )
                    file_bytes = await response["Body"].read()
            else:
                path = key.removesuffix(f".{ext}")
                file_bytes = await self.read_volume_file(path=path)

        except Exception:
            logger.debug(f"download_file_to_bytes: failed to download file {file_id}")
            raise_http_error(ErrorCode.OBJECT_NOT_FOUND, "Failed to download file")

        # create directory if not exists
        file_dir = file_path[: file_path.rfind("/")]
        if not await aiofiles.os.path.exists(file_dir):
            await aiofiles.os.makedirs(file_dir)

        # save file
        try:
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(file_bytes)
                logger.debug(f"download_file_to_path: saved Minio file {file_id} to {file_path}")
            return True
        except Exception as e:
            logger.error(f"download_file_to_path: failed to save Minio file {file_id} to {file_path}, e={e}")

        return False

    def get_file_url(
        self,
        bucket_name: str,
        purpose: str,
        file_id: str,
        tenant_id: str,
    ) -> str:
        """
        Get file url from minio
        :param bucket_name: the name of the bucket
        :param purpose: the purpose of the file
        :param file_id: the id of the file, e.g. txt_x123456
        :param tenant_id: the id of the tenant. Error will be raised if the tenant_id is not valid
        :return: the url of the file
        """

        ext, _id = _validate_file_id(file_id)
        key = _object_key(purpose, _id, ext, tenant_id)
        if self._is_s3:
            domain = self._bucket_public_domain or f"{self._endpoint_url}/{bucket_name}"
            return f"{domain}/{key}"

        path = key.removesuffix(f".{ext}")
        file_path = f"{self._volume}/{path}"
        files = os.listdir(file_path)
        file: str = next(f for f in files if os.path.isfile(os.path.join(file_path, f)))
        return f"{self._host_url}/{path}/{file}"

    async def delete_file(
        self,
        bucket_name: str,
        purpose: str,
        file_id: str,
        tenant_id: str,
    ) -> bool:
        """
        Delete file from minio
        :param bucket_name: the name of the bucket
        :param purpose: the purpose of the file
        :param file_id: the id of the file, e.g. txt_x123456
        :param tenant_id: the id of the tenant. Error will be raised if the tenant_id is not valid
        :return: True if the file is deleted successfully, False otherwise
        """

        ext, _id = _validate_file_id(file_id)
        key = _object_key(purpose, _id, ext, tenant_id)
        if not await self.check_file_exists(bucket_name, purpose, file_id, tenant_id):
            raise_http_error(ErrorCode.OBJECT_NOT_FOUND, f"File {file_id} not found")
        try:
            if self._is_s3:
                async with self._session.client(
                    service_name=self._service_name, endpoint_url=self._endpoint_url
                ) as client:
                    await client.delete_object(
                        Bucket=bucket_name,
                        Key=key,
                    )
            else:
                path = key.removesuffix(f".{ext}")
                await self.delete_volume_file(path=path)
            return True
        except Exception as e:
            logger.error(f"delete_file: failed to delete file {file_id}, e={e}")
            return False

    def get_volume_file_abs_path(self, path):
        """
        Get absolute path of file in volume
        :param path: the path of the file
        :return: the absolute path of the file
        """
        file_path = f"{self._volume}/{path}"
        files = os.listdir(file_path)
        file: str = next(f for f in files if os.path.isfile(os.path.join(file_path, f)))
        return f"{self._volume}/{path}/{file}"

    async def save_to_volume(
        self,
        file_bytes: bytes,
        path: str,
    ):
        """
        Save file to volume
        :param file_bytes: the content of the file
        :param path: the path of the file
        """
        if self._volume:
            # create directory if not exists
            file_path = f"{self._volume}/{path}"
            file_dir = file_path[: file_path.rfind("/")]
            if not await aiofiles.os.path.exists(file_dir):
                await aiofiles.os.makedirs(file_dir)
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(file_bytes)
        else:
            raise ValueError("PATH_TO_VOLUME is not set")

    async def check_volume_file_exists(
        self,
        path: str,
    ):
        """
        Check if file exists
        :param path: the path of the file
        """
        try:
            file_path = f"{self._volume}/{path}"
            files = os.listdir(file_path)
            num_files = len([f for f in files if os.path.isfile(os.path.join(file_path, f))])
            if num_files == 1:
                return
            raise FileNotFoundError
        except FileNotFoundError:
            raise FileNotFoundError(f"File {path} not found")

    async def read_volume_file(
        self,
        path: str,
    ) -> bytes:
        """
        Read file from volume
        :param path: the path of the file
        """
        if self._volume:
            file_abs_path = self.get_volume_file_abs_path(path)
            async with aiofiles.open(file_abs_path, mode="rb") as f:
                return await f.read()
        else:
            raise ValueError("PATH_TO_VOLUME is not set")

    async def delete_volume_file(
        self,
        path: str,
    ):
        """
        Delete file from volume
        :param path: the path of the file
        """
        if self._volume:
            file_path = f"{self._volume}/{path}"
            files = os.listdir(file_path)
            for f in files:
                file_abs_path = os.path.join(file_path, f)
                await aiofiles.os.remove(file_abs_path)
                logger.debug(f"Delete volume file: {file_abs_path}")
            await aiofiles.os.removedirs(f"{self._volume}/{path}")
        else:
            raise ValueError("PATH_TO_VOLUME is not set")

    async def get_volume_file_metadata(
        self,
        path: str,
    ) -> Dict:
        """
        Get file metadata from volume
        :param path: the path of the file
        """
        if self._volume:
            file_path = f"{self._volume}/{path}"
            files = os.listdir(file_path)
            file: str = next(f for f in files if os.path.isfile(os.path.join(file_path, f)))
            file_size = await aiofiles.os.path.getsize(file_path)
            return {"original_file_name": file, "file_size": file_size}
        raise ValueError("PATH_TO_VOLUME is not set")
