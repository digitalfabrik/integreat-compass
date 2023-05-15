from django.db import models
from django.utils.translation import gettext_lazy as _

from ..abstract_base_model import AbstractBaseModel
from ..offers.offer_version import OfferVersion


class Report(AbstractBaseModel):
    """
    Data model representing a Report.
    """

    offer_version = models.ForeignKey(OfferVersion, on_delete=models.CASCADE)
    comment = models.TextField(
        verbose_name=_("comment"), help_text=_("Reason for the report")
    )

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``Report object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the page
        :rtype: str
        """
        return f"Report of {self.offer_version}"

    def get_repr(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<Report: Report object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the page
        :rtype: str
        """
        return f"<Report (id: {self.id}, offer: {self.offer}, offer_version: {self.offer_version})>"

    class Meta:
        verbose_name = _("report")
        verbose_name_plural = _("reports")
        default_related_name = "reports"
        default_permissions = ("change", "delete", "view")
