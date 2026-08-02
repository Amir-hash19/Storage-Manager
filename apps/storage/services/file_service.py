from apps.storage.repositories.file_repository import FileRepository



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