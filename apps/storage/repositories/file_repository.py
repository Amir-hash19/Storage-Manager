from apps.storage.models import File, FileStatus




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
    def create(**kwargs)-> File:
        return File.objects.create(**kwargs)