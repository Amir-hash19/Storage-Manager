from django.db import transaction
from apps.accounts.repositories.user_repository import UserRepository
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.exceptions import (
UserNameAlreadyExists, UserEmailAlreadyExists, InactiveUser,
InvalidCredentials)
from core.events import EventBus

from apps.accounts.events.user_event import UserLoggedInEvent


class LoginUserService:
    
    @transaction.atomic
    def execute(self, data):

        user = UserRepository.get_by_email(data["email"])
        
        if user is None:
            raise InvalidCredentials()

        if not user.check_password(data["password"]):
            raise InvalidCredentials()
        
        if not user.is_active:
            raise InactiveUser()
        
        refresh = RefreshToken.for_user(user)

        EventBus.publish(
            UserLoggedInEvent(
                user_id=user.id,
                email=user.email
            )
        )

        return {
            "user":user,
            "access":str(refresh.access_token),
            "refresh": str(refresh)
        }