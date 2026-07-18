from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from django.urls import path
from .views import RegisterView, LoginView, ChangePasswordView, RetrieveUserView, LogOutView, ForgotPasswordView, ResetPasswordView


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
    ),
    path(
        "password/",
        ForgotPasswordView.as_view(),
        name="forget-password"
    ),
    path(
        "reset-password/",
        ResetPasswordView.as_view(),
        name="reset-password"
    ),
    
    path("verify-token/", TokenVerifyView.as_view(), name="verify-token"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh-token")

]