from django.shortcuts import render
from django.views.generic import ListView

from ..constants import offer_group_types, offer_mode_types
from ..models import Offer, Tag


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

    def get_context_data(self, **kwargs):
        """
        This functions displays all offers
        :param kwargs: The supplied keyword arguments
        :type kwargs: dict

        :return: The context of all
        :rtype: dict
        """
        offers = Offer.objects.all()
        tags = Tag.objects.all()
        context = {
            "tags": tags,
            "offers": offers,
            "offer_group_types": offer_group_types.CHOICES,
            "offer_mode_types": offer_mode_types.CHOICES,
        }
        return context

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

        if request.GET.get("free_offer"):
            filtered_offers = filtered_offers.filter(versions__is_free=True)

        return render(
            request,
            self.template_name,
            {
                "tags": Tag.objects.all(),
                "offers": [
                    offer
                    for offer in filtered_offers.distinct()
                    if offer.public_version
                ],
                "filtered_tags": offer_tags,
                "offer_group_types": offer_group_types.CHOICES,
                "filtered_group_types": group_types,
                "offer_mode_types": offer_mode_types.CHOICES,
                "filtered_mode_types": mode_types,
                "filtered_free_offer": bool(request.GET.get("free_offer")),
            },
        )
