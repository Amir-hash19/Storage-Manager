from rest_framework.exceptions import ValidationError

from apps.storage.models import Folder

from apps.storage.repositories.folder_repository import FolderRepository




class FolderService:

    @staticmethod
    def create_folder(
        *,
        owner,
        name: str,
        parent_id=None
    ) -> Folder:
        parent = None

        if parent_id:

            parent = FolderRepository.get_by_id(parent_id)

            if parent is None:
                raise ValidationError(
                    {"parent_id": "Folder not found."}
                )

            if parent.owner != owner:
                raise ValidationError(
                    {"parent_id":"Invalid parent Folder."}
                )

        if FolderRepository.exists(
            owner=owner,
            parent=parent,
            name=name
        ):
            raise ValidationError(
                {"detail":"Folder with this name already exists."}
            )    
        
        path = (
            f"{parent.path}/{name}"
            if parent
            else name
        )
            
        folder = FolderRepository.create(
            owner=owner,
            parent=parent,
            name=name,
            path=path
        )

        return folder