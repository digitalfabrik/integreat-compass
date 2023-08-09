import logging

from django.conf import settings
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext as _

from .token_generator import (
    account_activation_token_generator,
    password_reset_token_generator,
)

logger = logging.getLogger(__name__)


def send_mail(
    subject, email_template_name, html_email_template_name, context, recipient
):
    """
    Sends welcome email to user with new account.

    Making use of  :class:`~django.core.mail.EmailMultiAlternatives`
    to send a multipart email with plain text and html version.

    :param subject: The subject of the email
    :type subject: str

    :param email_template_name: The template to be used to render the text email
    :type email_template_name: str

    :param html_email_template_name: The template to be used to render the HTML email
    :type html_email_template_name: str

    :param subject: The subject of the email
    :type subject: str

    :param context: The template context variables
    :type context: dict

    :param recipient: The email address of the recipient
    :type recipient: str
    """
    context.update({"base_url": settings.BASE_URL})

    body = render_to_string(email_template_name, context)
    email = EmailMultiAlternatives(subject=subject, body=body, to=[recipient])
    email.mixed_subtype = "related"

    html_message = render_to_string(html_email_template_name, context)
    email.attach_alternative(html_message, "text/html")

    email.send()


def send_activation_mail(user):
    """
    Send an activation email to a newly registered user

    :param user: the newly registered user
    :type user: ~integreat_compass.cms.models.user.User
    """
    context = {"user": user}
    subject = _("Integreat Compass | Activate your account")

    token = account_activation_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    debug_mail_type = _("activation mail")
    context.update({"uid": uid, "token": token})

    try:
        send_mail(
            subject,
            "emails/activation_email.txt",
            "emails/activation_email.html",
            context,
            user.email,
        )
        logger.debug(
            "Sent a %r with an activation link to %r", debug_mail_type, user.email
        )
    except BadHeaderError as e:
        logger.exception(e)


def send_reset_mail(user):
    """
    Send a passwordf reset email to a user

    :param user: the user
    :type user: ~integreat_compass.cms.models.user.User
    """
    context = {"user": user}
    subject = _("Integreat Compass | Your requested password reset")

    token = password_reset_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    debug_mail_type = _("password reset mail")
    context.update({"uid": uid, "token": token})

    try:
        send_mail(
            subject,
            "emails/password_reset_email.txt",
            "emails/password_reset_email.html",
            context,
            user.email,
        )
        logger.debug(
            "Sent a %r with a password reset link to %r", debug_mail_type, user.email
        )
    except BadHeaderError as e:
        logger.exception(e)
