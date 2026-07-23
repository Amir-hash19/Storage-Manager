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