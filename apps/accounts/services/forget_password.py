from django.db import transaction
from apps.accounts.repositories.user_repository import UserRepository
from apps.accounts.exceptions import OldPasswordMatchNewPassword,PasswordsNotMatch,InvalidCurrentPassword, UserNameAlreadyExists, UserEmailAlreadyExists

from core.events import EventBus

from apps.accounts.events.user_event import UserChangedPasswordEvent

from django.contrib.auth.password_validation import validate_password
