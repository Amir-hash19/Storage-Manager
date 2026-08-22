from django.contrib.auth.hashers import make_password

from apps.storage.repositories.share_repository import ShareLinkRepository


class ShareLinkService:

    def __init__(self, repository=None):
        self.repository = repository or ShareLinkRepository()


    def create_share_link(
            self,
            *,
            file,
            user,
            password="",
            expires_at=None,
            max_downloads=0
    ):
        if file.owner_id != user.id:
            raise PermissionError(
                "You do not have permission to share this file."
            )
            
        if max_downloads < 0:
            raise ValueError(
                "max downloads cannot be negative."
            )    
        
        hashed_password = ""

        if password:
            hashed_password = make_password(password)

        return self.repository.create(
            file=file,
            created_by=user,
            password=hashed_password,
            expires_at=expires_at,
            max_downloads=max_downloads,
        )    