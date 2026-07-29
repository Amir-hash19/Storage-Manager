from django.urls import path


from .views import DashboardUsersView, DashboardStorageView

urlpatterns = [
    path(
        "user-statics/",
        DashboardUsersView.as_view(),
        name="user-statics"
        ),

    path(
        "users/storage/",
        DashboardStorageView.as_view(),
        name="storage-statics"
    )    
]