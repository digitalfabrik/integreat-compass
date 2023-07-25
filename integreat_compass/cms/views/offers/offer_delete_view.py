import logging

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import DeleteView

from ...models import Offer

logger = logging.getLogger(__name__)


class OfferDeleteView(PermissionRequiredMixin, DeleteView):
    """
    View showing all of a user's offers
    """

    model = Offer
    http_method_names = ["post"]
    success_url = reverse_lazy("cms:protected:my_offers")

    def get_permission_required(self):
        if self.get_object().creator != self.request.user:
            raise PermissionDenied()
        return ["cms.change_offer"]

    def form_valid(self, form, *args, **kwargs):
        messages.success(
            self.request,
            _('The offer "{}" has successfully been deleted.').format(
                self.object.latest_version.title
            ),
        )
        return super().form_valid(form)
