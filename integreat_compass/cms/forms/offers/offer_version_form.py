import logging

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from ...models import Document, OfferVersion
from ..custom_model_form import CustomModelForm

logger = logging.getLogger(__name__)


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    """
    Custom CheckboxSelectMultiple child class which styles the checkboxes
    so that only deselection is possible
    """

    template_name = "offers/document_deletion.html"


class CustomImageField(forms.ClearableFileInput):
    """
    Custom ClearableFileInput child class which adds image preview and
    image removal functionality
    """

    template_name = "offers/image_picker.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["default_title_image"] = settings.DEFAULT_TITLE_IMAGE
        return context


class OfferVersionForm(CustomModelForm):
    """
    Form for creating and editing offer versions
    """

    prefix = "offer_version"
    documents_to_remove = forms.ModelMultipleChoiceField(
        widget=CustomCheckboxSelectMultiple(), queryset=None, required=False
    )

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        model = OfferVersion
        fields = ["title", "title_image", "description", "language", "is_free"]
        widgets = {
            "title_image": CustomImageField,
            "is_free": forms.Select(choices=((True, _("Yes")), (False, _("No")))),
        }

    def __init__(self, *args, **kwargs):
        r"""
        Initialize offer version form

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict
        """
        super().__init__(*args, **kwargs)
        self.fields["documents_to_remove"].queryset = (
            self.instance.documents
            if self.instance.pk is not None
            else Document.objects.none()
        )

    def clean(self):
        """
        Validate form fields which depend on each other, see :meth:`django.forms.Form.clean`:

        :return: The cleaned form data
        :rtype: dict
        """
        cleaned_data = super().clean()
        if cleaned_data["title_image"] is False:
            cleaned_data["title_image"] = settings.DEFAULT_TITLE_IMAGE
        return cleaned_data

    def save(self, commit=True):
        """
        This method extends the default ``save()``-method of the base :class:`~django.forms.ModelForm`
        to manage the ManyToMany relation with :class:`~integrat_compass.cms.models.offers.document.Document`.

        :param commit: Whether or not the changes should be written to the database
        :type commit: bool

        :return: The saved region object
        :rtype: ~integreat_cms.cms.models.offers.offer_version.OfferVersion
        """
        offer_version = super().save(commit=commit)
        for document in self.cleaned_data["documents_to_remove"]:
            document.offer_versions.remove(offer_version)

        return offer_version
