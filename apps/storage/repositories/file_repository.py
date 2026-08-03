from apps.storage.models import File, FileStatus
from django.db.models import QuerySet




class FileRepository:

    @staticmethod
    def get_by_folder(folder):
        return (
            File.objects
            .filter(
                folder=folder,
                status=FileStatus.ACTIVE
            )
            .order_by("file_name")
        )

    @staticmethod
    def get_by_id(file_id):
        return (
            File.objects
            .select_related("owner", "folder")
            .filter(id=file_id)
            .first()
        )

    @staticmethod
    def exists(folder, file_name) -> bool:
        return File.objects.filter(
            folder=folder,
            file_name=file_name
        ).exists()

    @staticmethod
    def update_status(*, file, status):
        file.status = status
        file.save(update_fields=["status"])
        return file


    @staticmethod
    def update_storage_key(*, file, storage_key):
        file.storage_key = storage_key
        file.save(update_fields=["storage_key"])

        return file

    @staticmethod
    def hard_delete(file):
        file.delete()


    @staticmethod
    def get_active_by_id(file_id, owner):
        return (
            File.objects.select_related("owner", "folder")
            .filter(
                id=file_id,
                owner=owner,
                status=FileStatus.ACTIVE,
                
            )
            .first()
        )    

    @staticmethod
    def get_queryset(*, owner) -> QuerySet[File]:
        return (
            File.objects
            .select_related("folder")
            .filter(
                owner=owner,
                status=FileStatus.ACTIVE
            )
        )

    @classmethod
    def get_deleted_by_id(cls, *, owner, file_id):
        return (
            File.objects
            .select_related("folder")
            .filter(
                id=file_id,
                owner=owner,
                status=FileStatus.DELETED,
            )
            .first()
        )

    @staticmethod
    def save(*, file):
        file.save(update_fields=["status","updated_at"])    

        
    @staticmethod
    def create(**kwargs)-> File:
        return File.objects.create(**kwargs)




