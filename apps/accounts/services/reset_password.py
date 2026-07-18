from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

from apps.accounts.exceptions import (
    InvalidResetPasswordToken,
    ResetPasswordTokenExpired,
    ResetPasswordTokenAlreadyUsed,
    PasswordsNotMatch,
)

from apps.accounts.repositories.user_repository import PasswordResetRepository
from apps.accounts.repositories.user_repository import (
    UserRepository,
)

from apps.accounts.events.user_event import UserChangedPasswordEvent
from core.events import EventBus


class ResetPasswordService:

    @staticmethod
    def is_expired(reset_token):
        return reset_token.expires_at < timezone.now()

    @staticmethod
    def execute(
        token: str,
        password: str,
        confirm_password: str,
    ):

        if password != confirm_password:
            raise PasswordsNotMatch()

        reset_token = PasswordResetRepository.get_by_token(token)

        if reset_token is None:
            raise InvalidResetPasswordToken()

        if reset_token.used_at is not None:
            raise ResetPasswordTokenAlreadyUsed()

        if reset_token.expires_at < timezone.now():
            raise ResetPasswordTokenExpired()

        validate_password(
            password,
            reset_token.user,
        )

        reset_token.user.set_password(password)

        UserRepository.save(
            reset_token.user,
        )

        PasswordResetRepository.mark_as_used(
            reset_token,
        )

        EventBus.publish(
            UserChangedPasswordEvent(
                user_id=reset_token.user.id,
                email=reset_token.user.email,
                username=reset_token.user.username,
            )
        )

        return reset_token.user