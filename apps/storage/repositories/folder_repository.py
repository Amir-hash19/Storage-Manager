from apps.storage.models import Folder
from django.utils import timezone
from typing import Optional
from django.db.models import Q





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
    def get_by_id_owner(folder_id, owner):
        return Folder.objects.filter(
                id=folder_id, is_deleted=False, owner=owner
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
        ).update(is_deleted=True, deleted_at=timezone.now())


    @staticmethod
    def restore_descendants(folder):
        Folder.objects.filter(
            owner=folder.owner,
            path__startswith=folder.path,
            is_deleted=True
        ).update(
            is_deleted=False,
            deleted_at=None
        )

    @staticmethod
    def get_deleted_by_id(folder_id):
            return (
                Folder.objects.filter(
                    id=folder_id,
                    is_deleted=True
                )
                .select_related("owner", "parent")
                .first()
            )
    
    @staticmethod
    def get_deleted_folders(owner):
        return Folder.objects.filter(
            owner=owner,
            is_deleted=True
        )

    @staticmethod
    def hard_delete(queryset):
        queryset.delete()


    @staticmethod
    def list_trash(owner):
        return Folder.objects.filter(
            owner=owner,
            is_deleted=True,
        ).order_by("-deleted_at")


    @staticmethod
    def search_and_filter(
        owner,
        *,
        search=None,
        parent=None,
        deleted=False,
    ):
        queryset = Folder.objects.filter(
            owner=owner,
            is_deleted=deleted,
        )

        if parent:
            queryset = queryset.filter(parent_id=parent)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
            )

        return queryset.order_by("name")    

    


    @staticmethod
    def create(**kwargs):
        return Folder.objects.create(**kwargs)