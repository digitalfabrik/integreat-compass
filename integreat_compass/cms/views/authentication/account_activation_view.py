import logging

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _

from ...models import User
from ...utils.token_generator import account_activation_token_generator

logger = logging.getLogger(__name__)


class AccountActivationView(auth_views.PasswordResetConfirmView):
    """
    View to activate an account.
    """

    token_generator = account_activation_token_generator

    def dispatch(self, *args, **kwargs):
        r"""
        The view part of the view. Handles all HTTP methods equally.

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :return: The rendered template response or a redirection to the login page
        :rtype: ~django.template.response.TemplateResponse or ~django.http.HttpResponseRedirect
        """
        if self.request.user.is_authenticated:
            messages.success(self.request, _("You are already logged in."))
            return redirect("cms:public:index")

        user = User.objects.filter(
            pk=int(urlsafe_base64_decode(kwargs.get("uidb64")))
        ).first()
        if not user:
            messages.error(
                self.request,
                _("The account you are trying to activate does not exist."),
            )
            return redirect("cms:public:index")

        if self.token_generator.check_token(user, kwargs.get("token")):
            messages.success(
                self.request, _("Your account has been successfully activated.")
            )
            user.is_active = True
            user.save()
            logger.info("Account activation for user %r was successful", user)
            return redirect("cms:public:login")

        messages.error(
            self.request,
            " ".join(
                [
                    _("This account activation link is invalid."),
                    _("It may have already been used."),
                    _(
                        "Please contact an administrator to request a new link to activate your account."
                    ),
                ]
            ),
        )
        logger.debug("An invalid account activation link was used.")
        return redirect("cms:public:login")
