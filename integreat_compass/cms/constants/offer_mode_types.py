"""
This module contains all string representations of all mode types in which offers
can be offered, used by :class:`~integreat_compass.cms.models.offers.offer.Offer`
"""
from django.utils.translation import gettext_lazy as _

ONLINE = "ONLINE"
HYBRID = "HYBRID"
IN_PERSON = "IN_PERSON"

CHOICES = ((ONLINE, _("online")), (HYBRID, _("hybrid")), (IN_PERSON, _("in person")))
