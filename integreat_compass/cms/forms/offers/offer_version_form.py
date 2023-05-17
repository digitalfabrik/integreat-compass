import logging

from django import forms
from django.utils.translation import gettext_lazy as _

from ...models import OfferVersion
from ..custom_model_form import CustomModelForm

logger = logging.getLogger(__name__)


class OfferVersionForm(CustomModelForm):
    """
    Form for creating and editing offer versions
    """

    prefix = "offer_version"

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        model = OfferVersion
        fields = ["title", "description", "language", "is_free"]
        widgets = {
            "is_free": forms.Select(choices=((True, _("Yes")), (False, _("No"))))
        }
