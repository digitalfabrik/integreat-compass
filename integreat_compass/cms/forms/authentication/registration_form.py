import logging

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _

from ...constants import group_names
from ...models import User
from ..custom_model_form import CustomModelForm

logger = logging.getLogger(__name__)


class RegistrationForm(CustomModelForm):
    """
    Form for user self-registration as offer providers
    """

    password = forms.CharField(
        widget=forms.PasswordInput(), validators=[validate_password]
    )
    password_confirm = forms.CharField(
        label=_("Confirm password"), widget=forms.PasswordInput()
    )

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        model = User
        fields = ["email", "display_name"]

    def clean(self):
        """
        Validate form fields which depend on each other, see :meth:`django.forms.Form.clean`:
        If passwords do not match, add a :class:`~django.core.exceptions.ValidationError`.

        :return: The cleaned form data
        :rtype: dict
        """
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirm"):
            self.add_error(
                "password_confirm", forms.ValidationError(_("Passwords do not match."))
            )
        return cleaned_data

    def clean_email(self):
        """
        Ensure the email does not exist yet, see :ref:`overriding-modelform-clean-method`:
        If the email is already registered, add a :class:`~django.core.exceptions.ValidationError`.

        :return: The password
        :rtype: str
        """

        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).first():
            self.add_error(
                "email",
                forms.ValidationError(
                    _(
                        'An account for the email "{}" does already exist. Did you mean to log in?'
                    ).format(email)
                ),
            )
        return email

    def clean_display_name(self):
        """
        Ensure the display_name does not exist yet, see :ref:`overriding-modelform-clean-method`:
        If the display_name is already taken, add a :class:`~django.core.exceptions.ValidationError`.

        :return: The display_name
        :rtype: str
        """

        display_name = self.cleaned_data["display_name"]
        if User.objects.filter(display_name=display_name).first():
            self.add_error(
                "display_name",
                forms.ValidationError(
                    _('The display name "{}" is already taken.').format(display_name)
                ),
            )
        return display_name

    def save(self, commit=True):
        """
        This method extends the default ``save()``-method of the base :class:`~django.forms.ModelForm`
        to create a new non-active user with role Offer Provider.

        :param commit: Whether or not the changes should be written to the database
        :type commit: bool

        :return: The saved region object
        :rtype: ~integreat_compass.cms.models.offers.offer_version.OfferVersion
        """
        cleaned_data = self.cleaned_data
        new_user = User.objects.create_user(
            email=cleaned_data["email"],
            display_name=cleaned_data["display_name"],
            password=cleaned_data["password"],
            group=group_names.OFFER_PROVIDER,
            is_active=False,
        )

        logger.debug("Created new offer provider %s", self.cleaned_data["email"])
        return new_user
