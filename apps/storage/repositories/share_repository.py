from django.db import models 
from apps.storage.models import ShareLink





class ShareLinkRepository:

    def create(
            self,
            *,
            file,
            created_by,
            password="",
            expires_at=None,
            max_downloads=0
    ) -> ShareLink:
        return ShareLink.objects.create(
            file=file,
            created_by=created_by,
            password=password,
            expires_at=expires_at,
            max_downloads=max_downloads
        )
    
    def get_by_token(self, token):
        return (
            ShareLink.objects
            .select_related("file", "created_by")
            .filter(token=token)
            .first()
        )    
    
    def get_file_links(self, *, file, created_by):
        return ShareLink.objects.filter(
            file=file,
            created_by=created_by,
        )
    
    def deactivate(self, share_link):
        share_link.is_active = False
        share_link.save(update_fields=["is_active"])