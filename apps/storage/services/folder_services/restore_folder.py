from django.db import transaction
from apps.storage.repositories.folder_repository import FolderRepository
from apps.storage.exceptions import FolderNotFound, FolderAlreadyExists

class FolderRestoreService:

    @staticmethod
    @transaction.atomic
    def restore(folder_id, user):


        folder = FolderRepository.get_deleted_by_id(folder_id)

        if folder is None:
            raise FolderNotFound()

        if folder.owner != user:
            raise FolderNotFound()
            

        exists = FolderRepository.exists(
            owner=folder.owner,
            parent=folder.parent,
            name=folder.name,
        )

        if exists:
            raise FolderAlreadyExists()

        FolderRepository.restore_descendants(folder)