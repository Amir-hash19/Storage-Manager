from django.urls import path
from .views import RegisterView, LoginView, ChangePasswordView



urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password"
    )
]