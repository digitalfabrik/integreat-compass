from django.db import models
from django.utils.translation import gettext_lazy as _

from ..abstract_base_model import AbstractBaseModel
from ..users.user import User


class Contact(AbstractBaseModel):
    """
    Data model representing an Offer Contact.
    """

    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(
        max_length=255,
        verbose_name=_("name"),
        help_text=_("Name of the point-of-contact person"),
    )
    email = models.EmailField(
        verbose_name=_("email"),
        help_text=_("Email address of the point-of-contact person"),
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("phone number"),
        help_text=_("Phone numbner of the point-of-contact person"),
    )

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``Contact object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the page
        :rtype: str
        """
        return f"Contact {self.name}"

    def get_repr(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<Contact: Contact object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the page
        :rtype: str
        """
        return f"<Contact (id: {self.id}, name: {self.name})>"

    class Meta:
        verbose_name = _("offer contact")
        verbose_name_plural = _("offer contacts")
        default_related_name = "offer_contact"
        ordering = ["name"]
        default_permissions = ("change", "delete", "view")
