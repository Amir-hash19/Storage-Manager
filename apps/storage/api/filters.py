from django_filters import rest_framework as filters

from apps.storage.models import File


class FileFilter(filters.FilterSet):
    status = filters.CharFilter(field_name="status")
    folder = filters.NumberFilter(field_name="folder_id")

    class Meta:
        model = File
        fields = (
            "status",
            "folder",
        )