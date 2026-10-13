from math import sqrt

from django.conf import settings
from django.db.models import Prefetch, Q
from django.shortcuts import render
from django.views.generic import ListView

from ..constants import offer_group_types, offer_mode_types
from ..models import Comment, Offer, OfferVersion, Tag


def within_radius(offer_lat, offer_long, lat, long, radius):
    """
    Helper method to figure out if an offer is at maximum
    radius km from a pair of coordinates

    :param offer_lat: lat of the offer
    :type offer_lat: float

    :param offer_long: long of the offer
    :type offer_long: float

    :param lat: given latitude
    :type lat: float

    :param long: given longitude
    :type long: float

    :param radius: max distance between coordinates in km
    :type radius: int

    :return: whether the offer is within the given radius of the coordinates
    :rtype: bool
    """
    # Offers without coordinates (i.e. online-only offers) should not get filtered out
    # by the location filter. Users can do so explicitly with the mode filter.
    if not offer_lat or not offer_long:
        return True
    max_deg_difference = radius / 110.574
    return (
        sqrt((float(offer_lat) - lat) ** 2 + (float(offer_long) - long) ** 2)
        <= max_deg_difference
    )


class IndexListView(ListView):
    """
    View to see all offers
    """

    template_name = "index.html"
    context_object_name = "all_offers_list"

    def get_queryset(self):
        """
        Fetches all offers together with the related data needed to render them,
        so that iterating over the offers (and their versions) does not trigger
        a separate query per offer (N+1).

        :return: The offer queryset
        :rtype: ~django.db.models.query.QuerySet
        """
        return Offer.objects.select_related(
            "organization", "offer_contact", "location"
        ).prefetch_related(
            "tags",
            Prefetch(
                "versions",
                queryset=OfferVersion.objects.select_related(
                    "language"
                ).prefetch_related(
                    "documents",
                    Prefetch(
                        "comments", queryset=Comment.objects.select_related("creator")
                    ),
                ),
            ),
        ).order_by("id")

    def _filter_by_tags(self, queryset, tags):
        """
        :param queryset: The offer queryset to filter
        :type queryset: ~django.db.models.query.QuerySet

        :param tags: The tag ids to filter by
        :type tags: list

        :return: The filtered queryset
        :rtype: ~django.db.models.query.QuerySet
        """
        if not tags:
            return queryset
        return queryset.filter(tags__in=tags)

    def _filter_by_mode(self, queryset, mode_types):
        """
        :param queryset: The offer queryset to filter
        :type queryset: ~django.db.models.query.QuerySet

        :param mode_types: The mode types to filter by
        :type mode_types: list

        :return: The filtered queryset
        :rtype: ~django.db.models.query.QuerySet
        """
        if not mode_types:
            return queryset
        return queryset.filter(mode_type__in=mode_types)

    def _filter_by_group(self, queryset, group_types):
        """
        :param queryset: The offer queryset to filter
        :type queryset: ~django.db.models.query.QuerySet

        :param group_types: The group types to filter by
        :type group_types: list

        :return: The filtered queryset
        :rtype: ~django.db.models.query.QuerySet
        """
        if not group_types:
            return queryset
        return queryset.filter(group_type__in=group_types)

    def _filter_by_search(self, queryset, search):
        """
        :param queryset: The offer queryset to filter
        :type queryset: ~django.db.models.query.QuerySet

        :param search: The search term to filter by
        :type search: str

        :return: The filtered queryset
        :rtype: ~django.db.models.query.QuerySet
        """
        if not search:
            return queryset
        return queryset.filter(
            Q(versions__title__icontains=search)
            | Q(versions__description__icontains=search)
        )

    def _filter_by_free_offer(self, queryset, free_offer):
        """
        :param queryset: The offer queryset to filter
        :type queryset: ~django.db.models.query.QuerySet

        :param free_offer: Whether to filter for free offers only
        :type free_offer: bool

        :return: The filtered queryset
        :rtype: ~django.db.models.query.QuerySet
        """
        if not free_offer:
            return queryset
        return queryset.filter(versions__is_free=True)

    def _filter_by_radius(self, queryset, radius, lat, long):
        """
        :param queryset: The offer queryset to filter
        :type queryset: ~django.db.models.query.QuerySet

        :param radius: The max distance in km, as a string from the request
        :type radius: str

        :param lat: The latitude to filter by, as a string from the request
        :type lat: str

        :param long: The longitude to filter by, as a string from the request
        :type long: str

        :return: The offers within the given radius
        :rtype: list
        """
        if not (radius and lat and long):
            return queryset
        return [
            offer
            for offer in queryset
            if within_radius(
                offer.location.lat,
                offer.location.long,
                float(lat),
                float(long),
                float(radius),
            )
        ]

    def get(self, request, *args, **kwargs):
        """
        This functions filters

        :param request: The current request
        :type request: ~django.http.HttpRequest

        :param args: The supplied arguments
        :type args: list

        :param kwargs: The supplied keyword arguments
        :type kwargs: dict

        :return: Response for filtered offers
        :rtype: ~django.template.response.TemplateResponse
        """
        offer_tags = request.GET.getlist("tags")
        mode_types = request.GET.getlist("mode")
        group_types = request.GET.getlist("group")
        free_offers = bool(request.GET.get("free_offer"))
        radius = request.GET.get("radius")
        lat = request.GET.get("lat")
        long = request.GET.get("long")

        if offer_search := request.GET.get("search"):
            offer_search = offer_search.strip()

        filtered_offers = self.get_queryset()
        filtered_offers = self._filter_by_tags(filtered_offers, offer_tags)
        filtered_offers = self._filter_by_mode(filtered_offers, mode_types)
        filtered_offers = self._filter_by_group(filtered_offers, group_types)
        filtered_offers = self._filter_by_search(filtered_offers, offer_search)
        filtered_offers = self._filter_by_free_offer(filtered_offers, free_offers)

        # from here on out, take care to not duplicate offers!
        filtered_offers = filtered_offers.distinct()
        filtered_offers = self._filter_by_radius(filtered_offers, radius, lat, long)

        return render(
            request,
            self.template_name,
            {
                "tags": Tag.objects.all(),
                "offers": [offer for offer in filtered_offers if offer.public_version],
                "filtered_search": offer_search,
                "filtered_tags": offer_tags,
                "offer_group_types": offer_group_types.CHOICES,
                "filtered_group_types": group_types,
                "offer_mode_types": offer_mode_types.CHOICES,
                "filtered_mode_types": mode_types,
                "filtered_free_offer": free_offers,
                "offer_distance_steps": settings.OFFER_DISTANCE_STEPS,
                "filtered_radius": radius,
                "max_comment_length": settings.MAX_COMMENT_LENGTH,
            },
        )
