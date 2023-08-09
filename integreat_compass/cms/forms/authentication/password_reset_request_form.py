import logging

from django import forms
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


class PasswordResetRequestForm(forms.Form):
    """
    Form for user password resets
    """

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("Enter your email")})
    )
