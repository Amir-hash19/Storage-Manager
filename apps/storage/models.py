from django.db import models
from core.models.base import BaseModel
import uuid

class Folder(BaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    owner = models.ForeignKey(
        "accounts.UserAccount",
        on_delete=models.CASCADE,
        related_name="folders",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    name = models.CharField(max_length=255)

    path = models.CharField(
        max_length=1024,
        db_index=True,
    )

    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "folders"

        ordering = ("name",)

        constraints = [
            models.UniqueConstraint(
                fields=["owner", "parent", "name"],
                name="unique_folder_per_parent",
            )
        ]

        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["parent"]),
            models.Index(fields=["is_deleted"]),
            models.Index(fields=["owner", "parent"]),
        ]

    def __str__(self):
        return self.name



class FileStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    DELETED = "DELETED", "Deleted"
    PROCESSING = "PROCESSING", "Processing"
    FAILED = "FAILED", "Failed"



class File(BaseModel):
    owner = models.ForeignKey(
        "accounts.UserAccount",
        on_delete=models.CASCADE,
        related_name="files",
    )

    folder = models.ForeignKey(
        "storage.Folder",
        on_delete=models.CASCADE,
        related_name="files",
    )

    file_name = models.CharField(max_length=255)

    extension = models.CharField(
        max_length=15,
    )

    mime_type = models.CharField(
        max_length=120,
    )

    size = models.PositiveBigIntegerField()

    checksum = models.CharField(
        max_length=64,
        db_index=True,
    )

    storage_key = models.CharField(
        max_length=512,
        unique=True,
    )

    status = models.CharField(
    max_length=20,
    choices=FileStatus.choices,
    default=FileStatus.ACTIVE,
    )

    class Meta:
        db_table = "files"

        ordering = ("-created_at",)

        constraints = [
            models.UniqueConstraint(
                fields=["folder", "file_name"],
                name="unique_file_per_folder",
            )
        ]

        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["folder"]),
            models.Index(fields=["is_deleted"]),
            models.Index(fields=["owner", "folder"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.file_name






class ShareLink(BaseModel):
    file = models.ForeignKey(
        "storage.File",
        on_delete=models.CASCADE,
        related_name="share_links",
    )

    created_by = models.ForeignKey(
        "accounts.UserAccount",
        on_delete=models.CASCADE,
        related_name="created_links",
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    password = models.CharField(
        max_length=255,
        blank=True,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    download_count = models.PositiveIntegerField(
        default=0,
    )

    max_downloads = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )
   

    class Meta:
        db_table = "share_links"

        ordering = ("-created_at",)

        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["expires_at"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return str(self.token)