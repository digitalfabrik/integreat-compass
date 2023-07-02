"""
This module contains helpers for the account activation process
(also see :class:`~integreat_compass.cms.views.authentication.account_activation_view.AccountActivationView`).
"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    This token generator is identical to the default password reset token generator of :mod:`django.contrib.auth` with
    the exception of the used HMAC salt.
    This means password reset tokens are no longer accepted for the account activation and vice versa.
    """

    key_salt = "integreat_compass.cms.utils.account_activation_token_generator.AccountActivationTokenGenerator"


account_activation_token_generator = AccountActivationTokenGenerator()
