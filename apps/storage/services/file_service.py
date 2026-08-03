from apps.storage.repositories.file_repository import FileRepository
from django.db import transaction
from django.utils import timezone
from apps.storage.models import FileStatus
from apps.storage.exceptions import FileNotFound, FileNotFoundException

class FileService:

    @staticmethod
    
    def get_file(*, owner, file_id):
        return FileRepository.get_active_by_id(
            owner=owner,
            file_id=file_id
        )

    @staticmethod
    def get_files(*, owner):
        return FileRepository.get_queryset(owner=owner)



    @staticmethod
    @transaction.atomic
    def soft_delete(*, owner, file_id):

        file = FileRepository.get_active_by_id(
            owner=owner,
            file_id=file_id
        )

        if not file:
            raise FileNotFound()

        file.status = FileStatus.DELETED
        file.updated_at = timezone.now()

        FileRepository.save(file=file)

        return file


    @staticmethod
    @transaction.atomic
    def restore(*, owner, file_id):

        file = FileRepository.get_deleted_by_id(
            owner=owner,
            file_id=file_id
        )

        if not file:
            raise FileNotFound()

        if file.folder.deleted_at:
            raise FileNotFoundException()

        file.status = FileStatus.ACTIVE

        FileRepository.save(file=file)

        return file