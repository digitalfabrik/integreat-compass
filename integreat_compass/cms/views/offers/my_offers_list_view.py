import logging

from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic.list import ListView

from ...decorators import permission_required
from ...models import Offer

logger = logging.getLogger(__name__)


@method_decorator(permission_required("cms.change_offer"), name="dispatch")
class MyOffersListView(ListView):
    """
    View showing all of a user's offers
    """

    template_name = "offers/my_offers_list.html"
    model = Offer

    def get_queryset(self, *args, **kwargs):
        r"""
        Render list of a user's offers.

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :raises ~django.core.exceptions.PermissionDenied: If user does not have the permission to edit the specific page

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """
        return Offer.objects.filter(creator=self.request.user)

    def get_context_data(self, **kwargs):
        r"""
        Pass additional context data to the template.

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :return: The context dictionary
        :rtype: dict
        """

        context_data = super().get_context_data(**kwargs)
        context_data["fallback_title_image"] = settings.DEFAULT_TITLE_IMAGE
        return context_data
