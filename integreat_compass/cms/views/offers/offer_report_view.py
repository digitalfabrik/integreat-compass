import logging

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from ...forms import ReportForm
from ...models import Offer, OfferVersion

logger = logging.getLogger(__name__)


class OfferReportView(TemplateView):
    """
    View to report an offer
    """

    template_name = "offers/offer_report.html"

    def get_context_data(self, **kwargs):
        r"""
        Add context data for the offer report view

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :return: The context used in the offer report view
        :rtype: dict
        """
        return super().get_context_data(**kwargs) | {
            "selected_offer": get_object_or_404(Offer, id=kwargs.get("pk")),
            "form": ReportForm(),
        }

    def post(self, request, *args, **kwargs):
        r"""
        This functions handles the input from the report function

        :param request: The current request
        :type request: ~django.http.HttpRequest

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :return: Redirect to the index view
        :rtype: ~django.http.HttpResponseRedirect
        """
        offer = get_object_or_404(Offer, id=kwargs.get("pk"))
        form = ReportForm(data=request.POST)

        if not form.is_valid():
            form.add_error_messages(request)
            return render(
                request,
                self.template_name,
                {"form": form, **self.get_context_data(**kwargs)},
            )

        form.instance.offer_version = OfferVersion.objects.get(
            id=offer.public_version.id
        )
        form.save()

        messages.success(
            request,
            _(
                'Your report for offer "{}" has successfully been submitted and will be reviewed shortly.'
            ).format(offer.public_version.title),
        )

        return redirect("cms:public:index")
