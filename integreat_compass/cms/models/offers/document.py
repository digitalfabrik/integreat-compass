from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ...constants import allowed_media
from ..abstract_base_model import AbstractBaseModel
from ..validators import file_size_limit
from .offer_version import OfferVersion


class Document(AbstractBaseModel):
    """
    Data model representing a Language.
    """

    offer_versions = models.ManyToManyField(OfferVersion)
    file = models.FileField(
        upload_to="documents/", validators=[file_size_limit], verbose_name=_("file")
    )
    name = models.CharField(max_length=255, null=False)
    file_size = models.IntegerField(verbose_name=_("file size"))
    file_type = models.CharField(
        choices=allowed_media.CHOICES, max_length=128, verbose_name=_("file type")
    )

    @cached_property
    def url(self):
        """
        Returns the URL of the document

        :return: URL of the document
        :rtype: str
        """
        return settings.BASE_URL + self.file.url if self.file else None

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``Document object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the document
        :rtype: str
        """
        return self.name

    def get_repr(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<MediaFile: Document object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the document
        :rtype: str
        """
        file_path = f"path: {self.file.path}, " if self.file else ""
        return f"<Document (id: {self.id}, name: {self.name}, {file_path})>"

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")
        default_related_name = "documents"
        ordering = ["name"]
        default_permissions = ("change", "delete", "view")
        permissions = [("upload_document", "Can upload documents")]
