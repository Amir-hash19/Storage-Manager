from django.db import transaction
from apps.accounts.repositories.user_repository import UserRepository
from apps.accounts.exceptions import OldPasswordMatchNewPassword,PasswordsNotMatch,InvalidCurrentPassword, UserNameAlreadyExists, UserEmailAlreadyExists

from core.events import EventBus

from apps.accounts.events.user_event import UserChangedPasswordEvent

from django.contrib.auth.password_validation import validate_password


class ChangePasswordService:

    def execute(user, old_password, new_password, confirm_password):

        if not user.check_password(old_password):
            raise InvalidCurrentPassword()

        if new_password != confirm_password:
            raise PasswordsNotMatch()

        if old_password == new_password:
            raise OldPasswordMatchNewPassword()

        validate_password(new_password, user)
        user.set_password(new_password)

        UserRepository.save(user)

        EventBus.publish(
            UserChangedPasswordEvent(
                user_id=user.id,
                email=user.email,
                username=user.username
            )
        )

        return user