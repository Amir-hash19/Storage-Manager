from apps.storage.models import Folder

from typing import Optional





class FolderRepository:

    @staticmethod
    def get_by_id(folder_id):
        return Folder.objects.filter(id=folder_id, is_deleted=False).first()
    

    @staticmethod
    def exists(owner, parent, name):
        return Folder.objects.filter(
            owner=owner,
            parent=parent,
            name=name,
            is_deleted=False
        ).exists()
    
    @staticmethod
    def create(**kwargs):
        return Folder.objects.create(**kwargs)