from django.urls import path

from .views import MeView, SendCodeView, VerifyCodeView, login_page

urlpatterns = [
    path("me/", MeView.as_view(), name="users-me"),
    path("auth/send-code/", SendCodeView.as_view(), name="users-send-code"),
    path("auth/verify-code/", VerifyCodeView.as_view(), name="users-verify-code"),
    path("login/", login_page, name="users-login-page"),
]
