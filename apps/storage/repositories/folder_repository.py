from apps.storage.models import Folder

from typing import Optional





class FolderRepository:

    @staticmethod
    def get(folder_id, owner):
        return (
            Folder.objects.filter(
                id=folder_id,
                owner=owner,
                is_deleted=False
            )
            .first()
        )
    
    @staticmethod
    def get_children(folder):
        return (
            Folder.objects.filter(
                parent=folder,
                is_deleted=False
            )
            .order_by("name")
        )

    @staticmethod
    def get_by_id(folder_id):
        return Folder.objects.filter(
            id=folder_id, is_deleted=False
            ).select_related(
                "owner",
                "parent"
            ).first()
        
    @staticmethod
    def exists_by_name(owner, parent, name):
        return Folder.objects.filter(
            owner=owner,
            parent=parent,
            name=name,
            is_deleted=False,
        ).exists()    

    @staticmethod
    def get_descendants(folder):
        return list(
            Folder.objects.filter(
                owner=folder.owner,
                is_deleted=False,
                path__startswith=folder.path,
            ).exclude(
                id=folder.id,
            )
        )    

    @staticmethod
    def exists(owner, parent, name):
        return Folder.objects.filter(
            owner=owner,
            parent=parent,
            name=name,
            is_deleted=False
        ).exists()

    @staticmethod
    def save(folder):
        folder.save(
            update_fields=[
                "name",
                "path",
                "updated_at",
            ]
        )    

    @staticmethod
    def bulk_update_paths(folders):
        Folder.objects.bulk_update(
            folders,
            ["path", "updated_at"],
        )        


    @staticmethod
    def soft_delete(folder: Folder):
        folder.is_deleted = True
        folder.save(update_fields=["is_deleted"])    


    @staticmethod
    def soft_delete_descendants(folder):
        Folder.objects.filter(
            owner=folder.owner,
            path__startswith=folder.path,
            is_deleted=False,
        ).update(is_deleted=True)

    
    @staticmethod
    def create(**kwargs):
        return Folder.objects.create(**kwargs)