from apps.storage.repositories.folder_repository import FolderRepository


class ListFolderTrashService:

    @staticmethod
    def list_trash(user):
        return FolderRepository.list_trash(user)

    @staticmethod
    def search_and_filter(
        *,
        user,
        search=None,
        parent=None,
        deleted=False,
    ):
        return FolderRepository.search_and_filter(
            owner=user,
            search=search,
            parent=parent,
            deleted=deleted,
        )