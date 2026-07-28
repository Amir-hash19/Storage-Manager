from django.db import transaction
from apps.accounts.repositories.user_repository import UserRepository
from apps.storage.events.storage_event import FileUploadedEvent
from apps.storage.exceptions import FileNotFound
from apps.storage.models import FileStatus
from apps.storage.repositories.file_repository import FileRepository
from apps.storage.services.minIO.storage_service import MinioStorageService
from apps.storage.services.temp_file_service import TempFileService




class ProcessUploadService:

    @classmethod
    def process(
        cls,
        *,
        file_id,
        temp_path: str,
    ):
        from core.events import EventBus

        file = FileRepository.get_by_id(file_id)

        if file is None:
            TempFileService.delete(temp_path)
            raise FileNotFound()

        try:
            with TempFileService.open(temp_path) as file_obj:

                MinioStorageService().upload(
                    file_obj=file_obj,
                    storage_key=file.storage_key,
                    file_size=file.size,
                    content_type=file.mime_type,
                )

            

            with transaction.atomic():

                FileRepository.update_status(
                    file=file,
                    status=FileStatus.ACTIVE,
                )

                UserRepository.increase_used_storage(
                    user_id=file.owner_id,
                    size=file.size,
                )

            EventBus.publish(
                FileUploadedEvent(
                    file_id=file.id,
                    owner_id=file.owner_id,
                )
            )

        except Exception:

            FileRepository.update_status(
                file=file,
                status=FileStatus.FAILED,
            )

            raise

        finally:
            TempFileService.delete(temp_path)