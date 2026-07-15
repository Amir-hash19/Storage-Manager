from django.db import transaction
from apps.accounts.repositories.user_repository import UserRepository
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.exceptions import UserDoesNotExists, UserNameAlreadyExists, UserEmailAlreadyExists






class UserProfileService:

    def get_user_profile(self, user):
        return user