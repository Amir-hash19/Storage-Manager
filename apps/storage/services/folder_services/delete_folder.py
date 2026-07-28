from django.db import transaction


from apps.storage.repositories.folder_repository import FolderRepository
from apps.storage.exceptions import FolderNotFound




class FolderDeleteService:

    @staticmethod
    @transaction.atomic
    def delete(folder_id, user):

        folder = FolderRepository.get_by_id(
            folder_id=folder_id
        )

        if folder is None:
            raise FolderNotFound()

        if folder.owner != user:
            raise FolderNotFound()

        FolderRepository.soft_delete_descendants(folder)