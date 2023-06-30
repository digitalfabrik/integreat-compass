import logging

from django import forms
from django.utils.translation import gettext_lazy as _

from ...constants import offer_mode_types
from ...models import Location
from ..custom_model_form import CustomModelForm

logger = logging.getLogger(__name__)


class LocationForm(CustomModelForm):
    """
    Form for creating and editing locations
    """

    prefix = "location"

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        model = Location
        fields = ["address", "lat", "long"]
        widgets = {"address": forms.TextInput()}

    def __init__(self, *args, **kwargs):
        r"""
        Initialize offer version form

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict
        """
        super().__init__(*args, **kwargs)
        self.data = kwargs.get("data", [])

    def clean(self):
        """
        Validate form fields which depend on each other, see :meth:`django.forms.Form.clean`:
        If no address is given for a non-online offer, add a :class:`~django.core.exceptions.ValidationError`.

        :return: The cleaned form data
        :rtype: dict
        """
        cleaned_data = super().clean()
        if self.data["offer-mode_type"] == offer_mode_types.ONLINE:
            cleaned_data["address"] = None
            cleaned_data["lat"] = None
            cleaned_data["long"] = None
            return cleaned_data

        if any(not cleaned_data.get(field) for field in ["address", "lat", "long"]):
            self.add_error(
                "address", forms.ValidationError(_("A valid address is required."))
            )
        return cleaned_data
