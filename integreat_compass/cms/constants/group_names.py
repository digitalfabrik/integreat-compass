"""
This module contains the possible names of roles to make them translatable.
"""
from django.utils.translation import gettext_lazy as _

BOARD_MEMBER = "BOARD_MEMBER"
INTEGRATION_SPECIALIST = "INTEGRATION_SPECIALIST"
OFFER_PROVIDER = "OFFER_PROVIDER"

#: Choices for non-staff roles
CHOICES = [
    (BOARD_MEMBER, _("Board Member")),
    (INTEGRATION_SPECIALIST, _("Integration Specialist")),
    (OFFER_PROVIDER, _("Offer Provider")),
]
