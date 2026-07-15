from apps.accounts.repositories.user_repository import UserRepository
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.exceptions import UserDoesNotExists, UserNameAlreadyExists, UserEmailAlreadyExists






class AuthService:
    def logout(self, refresh_token: str) -> None:
        token = RefreshToken(refresh_token)

        token.blacklist()

