from django.conf import settings
from minio import Minio





client = Minio(
    endpoint="minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,
)