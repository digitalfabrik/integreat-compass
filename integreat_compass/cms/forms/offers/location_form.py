import logging

from django import forms

from ...models import Location
from ..custom_model_form import CustomModelForm

logger = logging.getLogger(__name__)


class LocationForm(CustomModelForm):
    """
    Form for creating and editing locations
    """

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        model = Location
        fields = ["address", "lat", "long"]
        widgets = {"address": forms.TextInput()}
