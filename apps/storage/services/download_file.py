from apps.storage.repositories.file_repository import FileRepository
from apps.storage.services.minIO.storage_service import MinioStorageService
from django.http import FileResponse

from apps.storage.exceptions import FileNotFound




class DownloadFileService:

    @staticmethod
    def execute(file_id, user):

        file = FileRepository.get_active_by_id(
            file_id=file_id,
            owner=user
        )

        if not file:
            raise FileNotFound("file nist! kiri")

        storage = MinioStorageService()

        stream = storage.download(
            storage_key=file.storage_key
        )

        response = FileResponse(
            stream,
            as_attachment=True,
            filename=file.file_name
        )
        response["Content-Type"] = file.mime_type
        response["Content-Length"] = file.size

        return response