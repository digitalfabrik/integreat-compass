import logging

from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from ...forms import RegistrationForm
from ...utils.email_utils import send_activation_mail

logger = logging.getLogger(__name__)


class RegistrationView(TemplateView):
    """
    View allowing new users to sign up as offer providers
    """

    template_name = "authentication/registration.html"

    def get(self, request, *args, **kwargs):
        r"""
        Render :class:`~integreat_compass.cms.forms.registration_form.RegistrationForm`,

        :param request: The current request
        :type request: ~django.http.HttpRequest

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """

        return render(
            request,
            self.template_name,
            {"form": RegistrationForm(), **self.get_context_data(**kwargs)},
        )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        r"""
        Submit :class:`~integreat_compass.cms.forms.registration_form.RegistrationForm`,

        :param request: The current request
        :type request: ~django.http.HttpRequest

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """
        form = RegistrationForm(data=request.POST)

        if not form.is_valid():
            form.add_error_messages(request)

            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "messages_suppressed": True,
                    **self.get_context_data(**kwargs),
                },
            )

        new_user = form.save()

        messages.success(
            request,
            _(
                'A confirmation email has been sent to "{}". Please click the link in the email to activate your account.'
            ).format(new_user.email),
        )

        send_activation_mail(new_user)
        return redirect("cms:public:login")
