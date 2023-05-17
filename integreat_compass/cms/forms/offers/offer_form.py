import logging

from django import forms

from ...models import Offer
from ..custom_model_form import CustomModelForm

logger = logging.getLogger(__name__)


class OfferForm(CustomModelForm):
    """
    Form for creating and editing offers
    """

    prefix = "offer"

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        model = Offer
        fields = ["tags", "group_type", "mode_type"]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(attrs={"class": "hidden peer"}),
            "group_type": forms.RadioSelect(attrs={"class": "hidden peer"}),
            "mode_type": forms.RadioSelect(attrs={"class": "hidden peer"}),
        }
