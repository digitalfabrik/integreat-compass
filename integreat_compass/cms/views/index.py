from functools import reduce

from django.shortcuts import render
from django.views.generic import ListView

from ..constants import offer_group_types, offer_mode_types
from ..models import Offer, Tag


class IndexListView(ListView):
    """
    View to see all offers
    """

    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        """
        This functions displays all offers

        :param request: The current request
        :type request: ~django.http.HttpRequest

        :param args: The supplied arguments
        :type args: list

        :param kwargs: The supplied keyword arguments
        :type kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """
        offers = Offer.objects.all()
        tags = Tag.objects.all()

        return render(
            request,
            self.template_name,
            {
                "tags": tags,
                "offers": offers,
                "offer_group_types": offer_group_types.CHOICES,
                "offer_mode_types": offer_mode_types.CHOICES,
            },
        )

    def post(self, request):
        """
        This functions filters

        :param request: The current request
        :type request: ~django.http.HttpRequest

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """
        tags = Tag.objects.all()
        filtered_offers = Offer.objects.all()
        if request.POST.getlist("offer-tags"):
            # filtered_offers = Offer.objects.filter(tags__in = request.POST.getlist("offer-tags")).distinct()
            filtered_offers = reduce(
                lambda filtered_offers, tag: filtered_offers.filter(tags=tag),
                request.POST.getlist("offer-tags"),
                filtered_offers,
            )
        if request.POST.get("mode-type"):
            filtered_offers = Offer.objects.filter(
                mode_type=request.POST.get("mode-type")
            ).distinct()
        if request.POST.get("group-type"):
            filtered_offers = Offer.objects.filter(
                group_type=request.POST.get("group-type")
            ).distinct()
        if request.POST.get("offer-search"):
            filtered_offers = Offer.objects.filter(
                versions__title__icontains=request.POST.get("offer-search")
            ).distinct()

        return render(
            request,
            self.template_name,
            {
                "offers": filtered_offers,
                "tags": tags,
                "offer_group_types": offer_group_types.CHOICES,
                "offer_mode_types": offer_mode_types.CHOICES,
            },
        )
