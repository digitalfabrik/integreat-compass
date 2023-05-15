from django.db import models
from django.utils.translation import gettext_lazy as _

from ..abstract_base_model import AbstractBaseModel


class Tag(AbstractBaseModel):
    """
    Data model representing a Tag.
    """

    title = models.CharField(
        max_length=32, verbose_name=_("tag"), help_text=_("Title of the tag")
    )

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``Tag object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the page
        :rtype: str
        """
        return f"Tag {self.title}"

    def get_repr(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<Tag: Tag object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the page
        :rtype: str
        """
        return f"<Tag (id: {self.id}, title: {self.title})>"

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")
        default_related_name = "tag"
        ordering = ["title"]
        default_permissions = ("change", "delete", "view")
