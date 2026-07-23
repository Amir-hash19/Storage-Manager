from rest_framework.exceptions import NotFound

from apps.storage.repositories.file_repository import FileRepository
from apps.storage.repositories.folder_repository import FolderRepository





class FolderContentService:

    @staticmethod
    def get_contents(*, owner, folder_id):

        folder = FolderRepository.get(
            folder_id=folder_id,
            owner=owner
        )

        if folder is None:
            raise NotFound("Folder not found.")
        
        folders = FolderRepository.get_children(folder)

        files = FileRepository.get_by_folder(folder)

        return {
            "current_folder": folder,
            "folders": folders,
            "files": files
        }