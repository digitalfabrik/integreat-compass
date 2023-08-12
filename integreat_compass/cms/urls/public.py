from django.contrib.auth import views as auth_views
from django.urls import include, path

from ..views import authentication, index, offers

urlpatterns = [
    path("", index.IndexListView.as_view(), name="index"),
    path(
        "offers/",
        include(
            [
                path(
                    "<int:pk>/",
                    include(
                        [
                            path(
                                "report/",
                                offers.OfferReportView.as_view(),
                                name="report_offer",
                            )
                        ]
                    ),
                )
            ]
        ),
    ),
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
                path(
                    "register/",
                    authentication.RegistrationView.as_view(),
                    name="register",
                ),
                path(
                    "reset-password/",
                    include(
                        [
                            path(
                                "",
                                authentication.PasswordResetRequestView.as_view(),
                                name="password_reset_request",
                            ),
                            path(
                                "<uidb64>/<token>/",
                                authentication.PasswordResetConfirmView.as_view(),
                                name="password_reset_confirm",
                            ),
                        ]
                    ),
                ),
                path(
                    "activate-account/<uidb64>/<token>/",
                    authentication.AccountActivationView.as_view(),
                    name="activate_account",
                ),
            ]
        ),
    ),
]
