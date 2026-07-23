from django.urls import path

from .views import CreateFolderView, FolderContentsView, RenameFolderView, FolderDeleteView



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
    )
]