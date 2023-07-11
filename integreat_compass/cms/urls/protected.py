"""
URLconf for login-protected views of the cms package.
"""
from django.urls import include, path

from ..views import interactions, offers

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
    ),
    path(
        "applications/",
        include(
            [
                path(
                    "votes/",
                    include(
                        [
                            path("", interactions.VoteFormView.as_view(), name="votes"),
                            path(
                                "<int:offer_version_id>/add_vote/",
                                interactions.VoteFormView.add_vote,
                                name="add_vote",
                            ),
                        ]
                    ),
                ),
                path("reports/", interactions.VoteFormView.as_view(), name="reports"),
                path("declined/", interactions.VoteFormView.as_view(), name="declined"),
            ]
        ),
    ),
]
