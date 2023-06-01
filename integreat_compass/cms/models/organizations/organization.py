from django.db import models
from django.utils.translation import gettext_lazy as _

from ..abstract_base_model import AbstractBaseModel
from ..users.user import User


class Organization(AbstractBaseModel):
    """
    Data model representing an Organization (Offer Provider).
    """

    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(
        max_length=255,
        verbose_name=_("organization name"),
        help_text=_("Name of the organization"),
    )
    web_address = models.URLField(
        verbose_name=_("website"),
        help_text=_("URL of the website or social media of the organization"),
    )

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``Organization object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the page
        :rtype: str
        """
        return f"Organization {self.name}"

    def get_repr(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<Organization: Organization object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the page
        :rtype: str
        """
        return f"<Organization (id: {self.id}, name: {self.name})>"

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")
        default_related_name = "organization"
        ordering = ["name"]
        default_permissions = ("change", "delete", "view")
