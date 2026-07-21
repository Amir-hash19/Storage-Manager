from django.urls import path

from .views import CreateFolderView



urlpatterns = [

    path(
        "folder/",
        CreateFolderView.as_view(),
        name="create-folder"
    )
]