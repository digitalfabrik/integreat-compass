from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ...constants import offer_version_states
from ..abstract_base_model import AbstractBaseModel
from ..validators import file_size_limit
from .language import Language


def get_default_language():
    """
    Helper function to get or create the default offer language.

    :return: pk of the default offer language
    :rtype: int
    """
    language, _ = Language.objects.get_or_create(
        native_name=settings.DEFAULT_OFFER_LANGUAGE["native_name"],
        defaults=settings.DEFAULT_OFFER_LANGUAGE,
    )
    return language.pk


class OfferVersion(AbstractBaseModel):
    """
    Data model representing a Language.
    """

    offer = models.ForeignKey(
        "Offer", on_delete=models.CASCADE, related_name="versions"
    )
    offer_version_date = models.DateTimeField(default=timezone.now, null=False)
    title = models.CharField(
        max_length=255, verbose_name=_("title"), help_text=_("Title of this offer")
    )
    title_image = models.ImageField(
        default=settings.DEFAULT_TITLE_IMAGE,
        blank=True,
        upload_to="images/",
        validators=[file_size_limit],
        verbose_name=_("title image"),
        help_text=_("Choose a title image for this offer"),
    )
    description = models.TextField(
        verbose_name=_("description"),
        help_text=_("Detailed information about the offer"),
    )
    is_free = models.BooleanField(
        default=True,
        verbose_name=_("Free offer"),
        help_text=_("Whether this offer is free or not"),
    )
    language = models.ForeignKey(
        Language,
        default=get_default_language,
        on_delete=models.CASCADE,
        verbose_name=_("Language"),
        help_text=_("The language being taught in this offer"),
    )
    state = models.BooleanField(
        choices=offer_version_states.CHOICES,
        default=offer_version_states.PENDING,
        null=True,
    )

    @cached_property
    def documents(self):
        """
        Returns all documents associated with this offer version.

        :return: A queryset of `Document` objects
        :rtype: ~django.db.models.query.QuerySet [ ~integreat_compass.cms.models.offers.document.Document ]
        """
        return self.documents.all()

    @cached_property
    def is_initial_version(self):
        """
        Check if this offer version is the first version for its corresponding offer.
        Also returns true if no approved version exists.

        :returns: True if this offer version is the first version for its corresponding offer, False otherwise.
        :rtype: bool
        """
        return self.offer.versions.count() == 1 or not self.offer.versions.filter(
            state=offer_version_states.APPROVED
        )

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``OfferVersion object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the page
        :rtype: str
        """
        return f"version {self.id} of offer {self.offer}"

    def get_repr(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<OfferVersion: OfferVersion object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the page
        :rtype: str
        """
        return f"<OfferVersion (id: {self.id}, offer: {self.offer})>"

    class Meta:
        verbose_name = _("offer version")
        verbose_name_plural = _("offer versions")
        default_related_name = "offer_versions"
        ordering = ["-offer_version_date"]
