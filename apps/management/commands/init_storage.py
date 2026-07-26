from django.conf import settings
from apps.storage.services.minIO.minio_client import client

bucket = settings.MINIO_BUCKET_NAME

if not client.bucket_exists(bucket):
    client.make_bucket(bucket)