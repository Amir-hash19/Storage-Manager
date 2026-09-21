from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.exceptions import (UserDoesNotExists,
                                      UserEmailAlreadyExists,
                                      UserNameAlreadyExists)
from apps.accounts.repositories.user_repository import UserRepository


class UserProfileService:

    def get_user_profile(self, user):
        return user
