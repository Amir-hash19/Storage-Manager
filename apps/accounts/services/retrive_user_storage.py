from apps.accounts.exceptions import UserDoesNotExists
from apps.accounts.repositories.user_repository import UserRepository






class RetrieveUserStorageService:

    @staticmethod
    def execute(user_id: int):

        storage = UserRepository.get_user_storage(user_id)


        if storage is None:
            raise UserDoesNotExists
        return storage
    
     