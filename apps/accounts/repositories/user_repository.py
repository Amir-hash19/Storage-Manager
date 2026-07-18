from apps.accounts.models import UserAccount
from apps.accounts.models import PasswordResetToken
from django.utils import timezone



class UserRepository:

    @staticmethod
    def get_by_id(self, user_id):
        return UserAccount.objects.filter(id=user_id).first()


    @staticmethod
    def exists_by_email(email: str) -> bool:
        return UserAccount.objects.filter(email=email).exists()
    
    @staticmethod
    def exists_by_username(username: str) -> bool:
        return UserAccount.objects.filter(username=username).exists()
    
    @staticmethod
    def get_by_email(email):
        return UserAccount.objects.filter(email=email).first()
    
    @staticmethod
    def save(user):
        user.save(update_fields=["password"])
    
    @staticmethod
    def create_user(**data)-> UserAccount:
        password = data.pop("password")
        user = UserAccount(**data)
        user.set_password(password)
        user.save()

        return user
    


class PasswordResetRepository:

    @staticmethod
    def create(*, user, token_hash: str, expires_at) -> PasswordResetToken:
        return PasswordResetToken.objects.create(
            user=user,
            token_hash=token_hash,
            expires_at=expires_at
        )
    
    @staticmethod
    def get_by_hash(token_hash: str):

        return (
            PasswordResetToken.objects
            .select_related("user")
            .filter(token_hash=token_hash)
            .first()
        )
    
    @staticmethod
    def delete_active_tokens(user):
        PasswordResetToken.objects.filter(
            user=user,
            used_at__isnull=True
        ).delete()

    @staticmethod
    def mark_as_used(token):

        token.used_at = timezone.now()

        token.save(update_fields=["used_at"])

        