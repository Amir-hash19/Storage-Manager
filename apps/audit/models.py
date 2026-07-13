import uuid
from django.db import models
from core.models.base import BaseModel


from .constants import (
    AuditAction,
    AuditResource,
    AuditStatus
)




class AuditLog(BaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        "accounts.UserAccount",
        on_delete=models.SET_NULL,
        related_name="audit_logs",
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=50,
        choices=AuditAction.choices
    )

    resource = models.CharField(
        max_length=30,
        choices=AuditResource.choices
    )

    resource_id = models.UUIDField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=AuditStatus.choices,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True
    )

    request_id = models.UUIDField(
        null=True,
        blank=True
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    changes = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        db_table = "audit_logs"

        ordering = ("-created_at",)

        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["action"]),
            models.Index(fields=["resource"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["request_id"]),
        ]

        
    def __str__(self):
        return f"{self.action} - {self.user}"    