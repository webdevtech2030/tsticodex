from django.urls import path
from django.views.generic import RedirectView

from .views import login_page

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="users-login-page", permanent=False)),
    path("login/", login_page, name="users-login-page"),
]
