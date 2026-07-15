from django.urls import path
from .views import RegisterView, LoginView, ChangePasswordView, RetrieveUserView, LogOutView


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
    ),

    path(
        "you/",
        RetrieveUserView.as_view(),
        name="retrieve-user-profile"
    ),

    path(
        "logout/",
        LogOutView.as_view(),
        name="user-logout"
    )

]