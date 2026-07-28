from apps.storage.repositories.folder_repository import FolderRepository






class FolderHardDeleteService:

    @staticmethod
    def empty_trash(user):

        folders = FolderRepository.get_deleted_folders(user)

        count = folders.count()

        FolderRepository.hard_delete(folders)

        return {
            "deleted_count": count
        }