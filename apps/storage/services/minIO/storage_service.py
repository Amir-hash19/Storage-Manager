from datetime import timedelta

from django.conf import settings
from minio import Minio
from minio.commonconfig import CopySource
from minio.error import S3Error

class StorageException(Exception):
    """Base exception for storage backend."""


class StorageUploadException(StorageException):
    pass


class StorageDeleteException(StorageException):
    pass


class StorageDownloadException(StorageException):
    pass


class StorageObjectNotFound(StorageException):
    pass

class MinioStorageService:

    def __init__(self):
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_SSL,
        )

        self.bucket = settings.MINIO_BUCKET_NAME

    # --------------------------------------------------
    # Upload
    # --------------------------------------------------

    def upload(
        self,
        *,
        file_obj,
        storage_key: str,
        file_size: int,
        content_type: str,
    ) -> str:

        try:
            self.client.put_object(
                bucket_name=self.bucket,
                object_name=storage_key,
                data=file_obj,
                length=file_size,
                content_type=content_type,
            )

            return storage_key

        except S3Error as exc:
            raise StorageUploadException(str(exc))

    # --------------------------------------------------
    # Download
    # --------------------------------------------------

    def download(
        self,
        *,
        storage_key: str,
    ):

        try:
            return self.client.get_object(
                bucket_name=self.bucket,
                object_name=storage_key,
            )

        except S3Error as exc:
            raise StorageDownloadException(str(exc))

    # --------------------------------------------------
    # Delete
    # --------------------------------------------------

    def delete(
        self,
        *,
        storage_key: str,
    ):

        try:
            self.client.remove_object(
                bucket_name=self.bucket,
                object_name=storage_key,
            )

        except S3Error as exc:
            raise StorageDeleteException(str(exc))

    # --------------------------------------------------
    # Exists
    # --------------------------------------------------

    def exists(
        self,
        *,
        storage_key: str,
    ) -> bool:

        try:
            self.client.stat_object(
                bucket_name=self.bucket,
                object_name=storage_key,
            )

            return True

        except S3Error:
            return False

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    def stat(
        self,
        *,
        storage_key: str,
    ):

        try:
            return self.client.stat_object(
                bucket_name=self.bucket,
                object_name=storage_key,
            )

        except S3Error:
            raise StorageObjectNotFound()

    # --------------------------------------------------
    # Presigned Url
    # --------------------------------------------------

    def generate_download_url(
        self,
        *,
        storage_key: str,
        expires: timedelta = timedelta(minutes=30),
    ) -> str:

        return self.client.presigned_get_object(
            bucket_name=self.bucket,
            object_name=storage_key,
            expires=expires,
        )

    # --------------------------------------------------
    # Copy
    # --------------------------------------------------

    def copy(
        self,
        *,
        source_key: str,
        destination_key: str,
    ):

        self.client.copy_object(
            bucket_name=self.bucket,
            object_name=destination_key,
            source=CopySource(
                self.bucket,
                source_key,
            ),
        )

    # --------------------------------------------------
    # Move
    # --------------------------------------------------

    def move(
        self,
        *,
        source_key: str,
        destination_key: str,
    ):

        self.copy(
            source_key=source_key,
            destination_key=destination_key,
        )

        self.delete(
            storage_key=source_key,
        )