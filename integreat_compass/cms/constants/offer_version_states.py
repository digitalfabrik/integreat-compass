"""
This module contains all string representations of all approval states of offer
versions, used by :class:`~integreat_compass.cms.models.offers.offer_version.OfferVersion`
"""
from django.utils.translation import gettext_lazy as _

REJECTED = False
APPROVED = True
PENDING = None

CHOICES = (
    (REJECTED, _("rejected")),
    (APPROVED, _("approved")),
    (PENDING, _("decision pending")),
)
