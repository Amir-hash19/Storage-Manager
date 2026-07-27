from dataclasses import dataclass
from uuid import UUID



@dataclass(slots=True)
class FileUploadRequestedEvent:
    file_id : UUID
    temp_path : str


@dataclass(slots=True)
class FileUploadedEvent:
    file_id : UUID
    owner_id : UUID