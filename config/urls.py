from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/accounts/", include("apps.accounts.api.urls")),
    path("api/storage/", include("apps.storage.api.urls"))
]

