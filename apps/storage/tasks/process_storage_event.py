from celery import shared_task

from apps.storage.services.upload_file_process import ProcessUploadService


@shared_task
def process_storage_event(*, event_name: str, payload: dict):

    match event_name:

        case "FileUploadRequestedEvent":

            ProcessUploadService.process(
                file_id=payload["file_id"],
                temp_path=payload["temp_path"],
            )

        case _:
            return