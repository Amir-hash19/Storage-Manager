from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileViewSet, DownloadfileView, FileUploadView,FolderListView, TrashFolderListView, EmptyTrashView, FolderRestoreView, CreateFolderView, FolderContentsView, RenameFolderView, FolderDeleteView

router = DefaultRouter()

router.register(
    "files",
    FileViewSet,
    basename="files"
)

urlpatterns = [

    path(
        "folder/",
        CreateFolderView.as_view(),
        name="create-folder"
    ),

    path(
        "folders/<uuid:folder_id>/contents/",
        FolderContentsView.as_view(),
        name="folders-content"
    ),

    path(
        "folders/<uuid:folder_id>/rename/",
        RenameFolderView.as_view(),
        name="rename-folder"
    ),

    path(
        "folders/<uuid:folder_id>/delete/",
        FolderDeleteView.as_view(),
        name="folder-delete-by-user"
    ),

    path(
        "folders/<uuid:folder_id>/restore/",
        FolderRestoreView.as_view(),
        name="folder-restore"
    ),

    path(
        "folders/trash/",
        EmptyTrashView.as_view(),
        name="empty-trash"
    ),

    path(
        "folders/trash/list/",
        TrashFolderListView.as_view(),
        name="trash-list-folders"

    ),

    path(
        "folders/list/",
        FolderListView.as_view(),
        name="folders-list"
    ),

    path(
        "file/upload/",
        FileUploadView.as_view(),
        name="file-upload"
    ),

    path(
        "file/download/<int:file_id>/",
        DownloadfileView.as_view(),
        name="download-file"
    ),

    path(
        "",
        include(router.urls)
    )
   
]