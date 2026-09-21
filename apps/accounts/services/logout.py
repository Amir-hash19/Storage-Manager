from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.exceptions import (UserDoesNotExists,
                                      UserEmailAlreadyExists,
                                      UserNameAlreadyExists)
from apps.accounts.repositories.user_repository import UserRepository


class AuthService:
    def logout(self, refresh_token: str) -> None:
        token = RefreshToken(refresh_token)

        token.blacklist()
