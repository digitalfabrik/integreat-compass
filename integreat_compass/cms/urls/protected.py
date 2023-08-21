"""
URLconf for login-protected views of the cms package.
"""
from django.urls import include, path

from ..views import components, interactions, offers

urlpatterns = [
    path(
        "offers/",
        include(
            [
                path("my/", offers.MyOffersListView.as_view(), name="my_offers"),
                path("new/", offers.OfferFormView.as_view(), name="new_offer"),
                path(
                    "<int:pk>/",
                    include(
                        [
                            path(
                                "edit/",
                                offers.OfferFormView.as_view(),
                                name="edit_offer",
                            ),
                            path(
                                "delete/",
                                offers.OfferDeleteView.as_view(),
                                name="delete_offer",
                            ),
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
                path("", interactions.VoteFormView.as_view(), name="votes"),
                path("reports/", components.ReportListView.as_view(), name="reports"),
                path(
                    "declined/", components.DeclineListView.as_view(), name="declined"
                ),
            ]
        ),
    ),
]
