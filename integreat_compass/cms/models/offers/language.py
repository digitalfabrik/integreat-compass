from django.db import models
from django.utils.translation import gettext_lazy as _

from ..abstract_base_model import AbstractBaseModel


class Language(AbstractBaseModel):
    """
    Data model representing a Language.
    """

    native_name = models.CharField(
        max_length=50,
        verbose_name=_("native name"),
        help_text=_("The name of the language in this language"),
    )
    english_name = models.CharField(
        max_length=50,
        verbose_name=_("name in English"),
        help_text=_("The name of the language in English"),
    )

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``Language object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the page
        :rtype: str
        """
        return f"Language: {self.english_name}"

    def get_repr(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<Language: Language object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the page
        :rtype: str
        """
        return f"<Language (id: {self.id}, language: {self.english_name})>"

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")
        default_related_name = "language"
        ordering = ["english_name"]
        default_permissions = ("change", "delete", "view")
