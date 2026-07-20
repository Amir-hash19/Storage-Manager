from apps.accounts.models import UserAccount
from apps.accounts.models import PasswordResetToken
from django.utils import timezone



class UserRepository:


    @staticmethod
    def get_user_storage(user_id: int):
        return UserAccount.objects.only(
                "storage_quota",
                "used_storage",
            ).filter(
                id=user_id
            ).first()
        

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
    
