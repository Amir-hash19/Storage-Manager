from django.db import transaction
from apps.accounts.repositories.user_repository import UserRepository, PasswordResetRepository
from apps.accounts.exceptions import OldPasswordMatchNewPassword,PasswordsNotMatch,InvalidCurrentPassword, UserNameAlreadyExists, UserEmailAlreadyExists
import hashlib
import secrets
from core.events import EventBus
from django.utils import timezone
from datetime import timedelta

from apps.accounts.events.user_event import PasswordResetRequestedEvent



class ForgetPasswordService:

    @transaction.atomic
    def execute(self, email:str):

        user = UserRepository.get_by_email(email)

        if not user:
            return 
        
        PasswordResetRepository.delete_active_tokens(user)

        raw_token = secrets.token_urlsafe(32)

        token_hash = hashlib.sha256(
            raw_token.encode()
        ).hexdigest()


        PasswordResetRepository.create(
            user=user,
            token_hash=token_hash,
            expires_at=timezone.now() + timedelta(minutes=20),
        )

        EventBus.publish(
            PasswordResetRequestedEvent(
                user_id=user.id,
                email=email,
                token=raw_token
            )
        )

