import logging

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
