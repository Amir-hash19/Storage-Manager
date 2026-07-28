
class FileNotFound(Exception):
    pass


class FolderNotFound(Exception):
    pass



class FolderAlreadyExists(Exception):
    pass



class FileAlreadyExists(Exception):
    pass



class StorageQuotaExceeded(Exception):
    pass




class StorageException(Exception):
    """Base exception for storage backend."""


class StorageUploadException(StorageException):
    pass


class StorageDeleteException(StorageException):
    pass


class StorageDownloadException(StorageException):
    pass


class StorageObjectNotFound(StorageException):
    pass