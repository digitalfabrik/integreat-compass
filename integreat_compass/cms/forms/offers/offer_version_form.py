import logging

from ...models import OfferVersion
from ..custom_model_form import CustomModelForm

logger = logging.getLogger(__name__)


class OfferVersionForm(CustomModelForm):
    """
    Form for creating and editing offer versions
    """

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        model = OfferVersion
        fields = ["title", "description", "language", "cost"]
