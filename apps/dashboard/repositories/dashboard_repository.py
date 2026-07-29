from apps.accounts.models import UserAccount,UserRole
from apps.storage.models import Folder, File, ShareLink, FileStatus

from django.db.models import Count, Q, Sum





class DashBoardRepository:

    @staticmethod
    def get_users_statistics():
        return UserAccount.objects.aggregate(
            total=Count("id"),
            active=Count("id", filter=Q(is_active=True)),
            verified=Count("id", filter=Q(is_verified=True)),
        )

    @staticmethod
    def get_storage_statistics():
        return UserAccount.objects.aggregate(
            used=Sum("used_storage"),
            quota=Sum("storage_quota"),
        )

    @staticmethod
    def get_files_statistics():
        File.objects.aggregate(
            total=Count("id"),
            active=Count("id", filter=Q(status=FileStatus.ACTIVE)),
            processing=Count("id", filter=Q(status=FileStatus.PROCESSING)),
            failed=Count("id", filter=Q(status=FileStatus.FAILED)),
            deleted=Count("id", filter=Q(status=FileStatus.DELETED)),
    )

    @staticmethod
    def get_folders_statistics():
        Folder.objects.aggregate(
            total=Count("id"),
            deleted=Count("id", filter=Q(is_deleted=True)),
    )

    @staticmethod
    def get_storage_summary():
        return UserAccount.objects.aggregate(
            quote=Sum("storage_quota"),
            used=Sum("used_storage"),
            users=Count("id")
        )

    @staticmethod
    def get_top_storage_users(limit=10):
        return (
            UserAccount.objects
            .order_by("-used_storage")
            .values(
                "id",
                "username",
                "used_storage",
            )[:limit]
        )

    

