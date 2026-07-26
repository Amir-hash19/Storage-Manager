from apps.storage.exceptions import StorageQuotaExceeded, FolderNotFound, FileAlreadyExists
import hashlib
from django.db import transaction
import uuid
from apps.storage.models import FileStatus

from apps.storage.repositories.folder_repository import FolderRepository
from apps.storage.repositories.file_repository import FileRepository
from django import Path


class UploadFileService:

    @staticmethod
    @transaction.atomic
    def upload(
        cls,
        *,
        owner,
        folder_id,
        uploaded_file
    ):
        folder = FolderRepository.get_by_id(
            folder_id=folder_id,
            owner=owner
        )

        if folder is None:
            raise FolderNotFound()

        exists = FileRepository.exists(
            folder=folder,
            file_name=uploaded_file.name
        )

        if exists:
            raise FileAlreadyExists()

        if owner.used_storage + uploaded_file.size > owner.storage_quota:
            raise StorageQuotaExceeded()

        checksum = cls._calculate_checksum(uploaded_file)

        extension = Path(uploaded_file.name).suffix.lower()    


        storage_key = cls._generate_storage_key(
            owner_id=owner.id,
            extension=extension,
        )


        file = FileRepository.create(
            owner=owner,
            folder=folder,
            file_name=uploaded_file.name,
            extension=extension,
            mime_type=uploaded_file.content_type,
            size=uploaded_file.size,
            checksum=checksum,
            storage_key=storage_key,
            status=FileStatus.PROCESSING,
        )


        @staticmethod
        def _calculate_checksum(uploaded_file):
            sha256 = hashlib.sha256()

            for chunk in uploaded_file.chunks():
                sha256.update(chunk)

            uploaded_file.seek(0)

            return sha256.hexdigest()

        @staticmethod
        def _generate_storage_key(
            *,
            owner_id,
            extension,
        ):
            return f"users/{owner_id}/{uuid.uuid4()}{extension}"