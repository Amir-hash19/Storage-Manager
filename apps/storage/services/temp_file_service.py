import os
import tempfile


class TempFileService:

    BASE_PATH = "/tmp/storage"


    @staticmethod
    def save(uploaded_file):

        os.makedirs(
            TempFileService.BASE_PATH,
            exist_ok=True
        )

        suffix = os.path.splitext(
            uploaded_file.name
        )[1]

        fd, path = tempfile.mkstemp(
            suffix=suffix,
            dir=TempFileService.BASE_PATH,
        )

        with os.fdopen(fd, "wb") as temp:

            for chunk in uploaded_file.chunks():
                temp.write(chunk)

        return path


    @staticmethod
    def open(path):
        return open(path, "rb")


    @staticmethod
    def delete(path):
        if os.path.exists(path):
            os.remove(path)