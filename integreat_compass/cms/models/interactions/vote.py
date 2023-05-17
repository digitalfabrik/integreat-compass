from django.db import models
from django.utils.translation import gettext_lazy as _

from ..abstract_base_model import AbstractBaseModel
from ..offers.offer_version import OfferVersion
from ..users.user import User


class Vote(AbstractBaseModel):
    """
    Data model representing a Vote.
    """

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    offer_version = models.ForeignKey(OfferVersion, on_delete=models.CASCADE)
    approval = models.BooleanField(
        verbose_name=_("approval"),
        help_text=_("Whether the vote approves or disapproves of an offer"),
    )
    comment = models.TextField(
        verbose_name=_("comment"),
        help_text=_("Reason for approving or disapproving an offer"),
    )

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``Vote object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the page
        :rtype: str
        """
        return f"Vote of user {self.creator} on {self.offer_version}"

    def get_repr(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<Vote: Vote object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the page
        :rtype: str
        """
        return f"<Vote (id: {self.id}, user: {self.creator}, offer_version: {self.offer_version})>"

    class Meta:
        unique_together = (("creator", "offer_version"),)
        verbose_name = _("vote")
        verbose_name_plural = _("votes")
        default_related_name = "votes"
        default_permissions = ("change", "delete", "view")
        permissions = [
            ("view_offer_votes", "View votes cast on offer version"),
            ("vote_on_offer", "Can cast vote on offer version"),
        ]
