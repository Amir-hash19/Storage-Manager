import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from core.models.base import BaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str | None = None, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )



class UserRole(models.TextChoices):
    OWNER = "owner", "Owner"
    PLATFORM_ADMIN = "platform_admin", "Platform Admin"


class UserAccount(AbstractBaseUser,
                  PermissionsMixin,
                   BaseModel
    ):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    email = models.EmailField(unique=True)

    username = models.CharField(max_length=150, unique=True)

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.OWNER
    )

    # 5GB
    storage_quota = models.BigIntegerField(
        default=5 * 1024 * 1024 * 1024
    )

    used_storage = models.BigIntegerField(
        default=0
    )


    is_verified = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    objects = CustomUserManager()


    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]

    class Meta:
        db_table = "users"

        ordering = ("-created_at",) 

        indexes = [
            models.Index(fields=["role"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_at"]),
            ]
        

       

    def __str__(self):
        return self.email    

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"    

