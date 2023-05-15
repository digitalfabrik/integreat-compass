"""
This module contains all string representations of all types of organizations,
used by :class:`~integreat_compass.cms.models.organizations.organization.Organization`
"""
from django.utils.translation import gettext_lazy as _

NON_PROFIT = "NON_PROVIT"
FOR_PROFIT = "FOR_PROFIT"
EV = "EV"

CHOICES = (
    (NON_PROFIT, _("non-profit")),
    (FOR_PROFIT, _("for-profit")),
    (EV, _("registered association")),
)
