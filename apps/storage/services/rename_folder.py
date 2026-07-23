from apps.storage.exceptions import FolderNotFound, FolderAlreadyExists
from apps.storage.repositories.folder_repository import FolderRepository
from django.db import transaction


class RenameFolderService:

    @staticmethod
    @transaction.atomic
    def execute(
        *,
        folder_id,
        owner,
        new_name
    ):
        folder = FolderRepository.get_by_id(folder_id)


        if not folder:
            raise FolderNotFound()

        if folder.owner_id != owner.id:
            raise FolderNotFound()

        new_name = new_name.strip()

        if folder.name == new_name:
            return folder

        exists = FolderRepository.exists_by_name(
            owner=owner,
            parent=folder.parent,
            name=new_name
        )

        if exists:
            raise FolderAlreadyExists()

        old_path = folder.path

        folder.name = new_name

        if folder.parent:
            folder.path = f"{folder.parent.path}{new_name}/"

        else:
            folder.path = f"{new_name}/"    

        FolderRepository.save(folder)


        descendants = FolderRepository.get_descendants(folder)

        for child in descendants:
            child.path = child.path.replace(
                old_path,
                folder.path,
                1,
            )
        if descendants:
            FolderRepository.bulk_update_paths(descendants)

        return folder    
