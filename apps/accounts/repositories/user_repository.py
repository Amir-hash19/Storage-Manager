from apps.accounts.models import UserAccount

class UserRepository:


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