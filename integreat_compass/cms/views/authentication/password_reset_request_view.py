import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView

from ...forms import PasswordResetRequestForm
from ...models import User
from ...utils.email_utils import send_reset_mail

logger = logging.getLogger(__name__)


class PasswordResetRequestView(FormView):
    """
    View allowing users to request a password reset
    """

    template_name = "authentication/password_reset_request.html"
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy("cms:public:login")

    def form_valid(self, form):
        r"""
        Overwrite the form_valid method to additionally send a reset email

        :param form: The user-submitted form
        :type form: ~integreat_compass.cms.forms.registration_form.RegistrationForm
        """
        response = super().form_valid(form)
        email = form.cleaned_data["email"]

        messages.success(
            self.request,
            _(
                'An email has been sent to "{}". Please use the link in the email to reset your password.'
            ).format(email),
        )

        if user := User.objects.filter(email__iexact=email).first():
            # Do nothing if the user does not exist.
            send_reset_mail(user)
        return response
