from math import sqrt

from django.conf import settings
from django.shortcuts import render
from django.views.generic import ListView

from ..constants import offer_group_types, offer_mode_types
from ..models import Offer, Tag


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
    max_deg_difference = radius / 110.574
    return sqrt((offer_lat - lat) ** 2 + (offer_long - long) ** 2) <= max_deg_difference


class IndexListView(ListView):
    """
    View to see all offers
    """

    template_name = "index.html"
    context_object_name = "all_offers_list"

    def get_queryset(self):
        """
        :return: The offer queryset
        :rtype: ~django.db.models.query.QuerySet
        """
        return Offer.objects.all()

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
        filtered_offers = Offer.objects.all()
        if offer_tags := request.GET.getlist("tags"):
            filtered_offers = filtered_offers.filter(tags__in=offer_tags)

        if mode_types := request.GET.getlist("mode"):
            filtered_offers = filtered_offers.filter(mode_type__in=mode_types)

        if group_types := request.GET.getlist("group"):
            filtered_offers = filtered_offers.filter(group_type__in=group_types)

        if offer_search := request.GET.get("search"):
            filtered_offers = filtered_offers.filter(
                versions__title__icontains=offer_search
            )
        if free_offers := bool(request.GET.get("free_offer")):
            filtered_offers = filtered_offers.filter(versions__is_free=True)

        # from here on out, take care to not duplicate offers!
        filtered_offers = filtered_offers.distinct()

        if (
            (radius := request.GET.get("radius"))
            and (lat := request.GET.get("lat"))
            and (long := request.GET.get("long"))
        ):
            filtered_offers = [
                offer
                for offer in filtered_offers
                if within_radius(
                    float(offer.location.lat),
                    float(offer.location.long),
                    float(lat),
                    float(long),
                    float(radius),
                )
            ]

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
            },
        )
