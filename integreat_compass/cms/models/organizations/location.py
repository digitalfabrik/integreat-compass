from django.db import models
from django.utils.translation import gettext_lazy as _

from ..abstract_base_model import AbstractBaseModel


class Location(AbstractBaseModel):
    """
    Data model representing a Location.
    """

    address = models.TextField(
        blank=False,
        null=False,
        verbose_name=_("address"),
        help_text=_("Physical location where the offer takes place"),
    )
    lat = models.DecimalField(
        max_digits=10, decimal_places=7, verbose_name=_("latitude")
    )
    long = models.DecimalField(
        max_digits=10, decimal_places=7, verbose_name=_("longitude")
    )

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``Location object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the page
        :rtype: str
        """
        return f"Location {self.address}"

    def get_repr(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<Location: Location object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the page
        :rtype: str
        """
        return f"<Location (id: {self.id}, address: {self.address})>"

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")
        default_related_name = "location"
        ordering = ["address"]
        default_permissions = ("change", "delete", "view")
