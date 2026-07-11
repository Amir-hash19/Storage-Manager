from django.db import transaction
from apps.accounts.repositories.user_repository import UserRepository
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.exceptions import UserNameAlreadyExists, UserEmailAlreadyExists



class RegisterUserService:

    @transaction.atomic
    def execute(self, data):
        
        if UserRepository.exists_by_email(data["email"]):
            raise UserEmailAlreadyExists()
        
        if UserRepository.exists_by_username(data["username"]):
            raise UserNameAlreadyExists()
        
        user = UserRepository.create_user(**data)

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }