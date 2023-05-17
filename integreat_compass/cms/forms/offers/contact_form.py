import logging

from ...models import Contact
from ..custom_model_form import CustomModelForm

logger = logging.getLogger(__name__)


class ContactForm(CustomModelForm):
    """
    Form for creating and editing offer contacts
    """

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        model = Contact
        fields = ["contact_name", "contact_email", "contact_phone"]
