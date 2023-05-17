import logging

from ...models import Organization
from ..custom_model_form import CustomModelForm

logger = logging.getLogger(__name__)


class OrganizationForm(CustomModelForm):
    """
    Form for creating and editing organizations
    """

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        model = Organization
        fields = ["org_name", "org_type", "web_address"]
