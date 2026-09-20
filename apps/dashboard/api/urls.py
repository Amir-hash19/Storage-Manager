from django.urls import path


from .views import liveness, readiness, DashboardUsersView, DashboardStorageView, DashboardAuditView

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
    ),

    path(
        "users/activities/",
        DashboardAuditView.as_view(),
        name="users-search-filters"
        
    ),

    path("liveness/", liveness, name="liveness-prob"),
    path("readiness/", readiness, name="readiness-prob")    
]