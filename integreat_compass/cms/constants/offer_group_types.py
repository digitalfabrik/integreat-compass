"""
This module contains all string representations of all group types in which offers
can be offered, used by :class:`~integreat_compass.cms.models.offers.offer.Offer`
"""
from django.utils.translation import gettext_lazy as _

PRIVATE = "PRIVATE"
GROUP = "GROUP"
BOTH = "BOTH"

CHOICES = ((PRIVATE, _("private")), (GROUP, _("group")), (BOTH, _("both")))
