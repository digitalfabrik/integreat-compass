from django.db import models
from django.utils.translation import gettext_lazy as _

from ..abstract_base_model import AbstractBaseModel
from ..offers.offer import Offer
from ..users.user import User


class Favorite(AbstractBaseModel):
    """
    Data model representing a Favorite.
    """

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``Favorite object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the page
        :rtype: str
        """
        return f"Favorite (user: {self.creator}, offer: {self.offer})"

    def get_repr(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<Favorite: Favorite object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the page
        :rtype: str
        """
        return f"<Favorite (id: {self.id}, user: {self.creator}, offer: {self.offer})>"

    class Meta:
        unique_together = (("creator", "offer"),)
        verbose_name = _("favorite")
        verbose_name_plural = _("favorites")
        default_related_name = "favorite"
        default_permissions = ("add", "delete", "view")
