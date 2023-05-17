"""
URLconf for login-protected views of the cms package.
"""
from django.urls import include, path

from ..views import offers

urlpatterns = [
    path(
        "offers/",
        include(
            [
                path("new/", offers.OfferFormView.as_view(), name="new_offer"),
                path(
                    "<int:pk>/",
                    include(
                        [
                            path(
                                "edit/",
                                offers.OfferFormView.as_view(),
                                name="edit_offer",
                            )
                        ]
                    ),
                ),
            ]
        ),
    )
]
