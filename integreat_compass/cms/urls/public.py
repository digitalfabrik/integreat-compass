from django.contrib.auth import views as auth_views
from django.urls import path

from ..views import index

urlpatterns = [
    path("", index.IndexView.as_view(), name="index"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
]
