from django.contrib.auth import views as auth_views
from django.urls import include, path

from ..views import index

urlpatterns = [
    path("", index.IndexView.as_view(), name="index"),
    path(
        "accounts/",
        include(
            [
                path(
                    "login/",
                    auth_views.LoginView.as_view(
                        template_name="authentication/login.html"
                    ),
                    name="login",
                ),
                path("logout/", auth_views.LogoutView.as_view(), name="logout"),
            ]
        ),
    ),
]
