from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CreateFolderView, DownloadfileView, EmptyTrashView,
                    FileDeleteView, FileRestoreView, FileUploadView,
                    FileViewSet, FolderContentsView, FolderDeleteView,
                    FolderListView, FolderRestoreView, RenameFolderView,
                    ShareLinkCreateAPIView, TrashFolderListView)

router = DefaultRouter()

router.register("files", FileViewSet, basename="files")

urlpatterns = [
    path("folder/", CreateFolderView.as_view(), name="create-folder"),
    path(
        "folders/<uuid:folder_id>/contents/",
        FolderContentsView.as_view(),
        name="folders-content",
    ),
    path(
        "folders/<uuid:folder_id>/rename/",
        RenameFolderView.as_view(),
        name="rename-folder",
    ),
    path(
        "folders/<uuid:folder_id>/delete/",
        FolderDeleteView.as_view(),
        name="folder-delete-by-user",
    ),
    path(
        "folders/<uuid:folder_id>/restore/",
        FolderRestoreView.as_view(),
        name="folder-restore",
    ),
    path("folders/trash/", EmptyTrashView.as_view(), name="empty-trash"),
    path(
        "folders/trash/list/", TrashFolderListView.as_view(), name="trash-list-folders"
    ),
    path("folders/list/", FolderListView.as_view(), name="folders-list"),
    path("file/upload/", FileUploadView.as_view(), name="file-upload"),
    path(
        "file/download/<int:file_id>/", DownloadfileView.as_view(), name="download-file"
    ),
    path("file/<int:file_id>/delete/", FileDeleteView.as_view(), name="file-delete"),
    path("file/<int:file_id>/restore/", FileRestoreView.as_view(), name="file-restore"),
    path(
        "files/<int:file_id>/share-links/",
        ShareLinkCreateAPIView.as_view(),
        name="create-share-links",
    ),
    path("", include(router.urls)),
]
