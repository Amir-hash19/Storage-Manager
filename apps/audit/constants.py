from django.db import models


class AuditAction(models.TextChoices):
    REGISTER = "REGISTER", "Register"
    LOGIN = "LOGIN", "Login"
    LOGOUT = "LOGOUT", "Logout"

    FILE_UPLOAD = "FILE_UPLOAD", "File Upload"
    FILE_DELETE = "FILE_DELETE", "File Delete"
    FILE_DOWNLOAD = "FILE_DOWNLOAD", "File Download"

    FOLDER_CREATE = "FOLDER_CREATE", "Folder Create"
    FOLDER_DELETE = "FOLDER_DELETE", "Folder Delete"

    SHARE_CREATE = "SHARE_CREATE", "Share Create"
    SHARE_DELETE = "SHARE_DELETE", "Share Delete"

    PASSWORD_CHANGE = "PASSWORD_CHANGE", "Password Change"


class AuditResource(models.TextChoices):
    USER = "USER", "User"
    FILE = "FILE", "File"
    FOLDER = "FOLDER", "Folder"
    SHARE = "SHARE", "Share"


class AuditStatus(models.TextChoices):
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"