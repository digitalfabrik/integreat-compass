from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ...constants import offer_group_types, offer_mode_types
from ..abstract_base_model import AbstractBaseModel
from ..interactions.comment import Comment
from ..users.user import User
from .tag import Tag


class Offer(AbstractBaseModel):
    """
    Data model representing an Offer.
    """

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    offer_contact = models.ForeignKey("Contact", on_delete=models.CASCADE)
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    group_type = models.CharField(
        choices=offer_group_types.CHOICES,
        default=offer_group_types.GROUP,
        verbose_name=_("group type"),
        help_text=_("Select in what group sizes lessons are offered"),
    )
    mode_type = models.CharField(
        choices=offer_mode_types.CHOICES,
        default=offer_mode_types.IN_PERSON,
        verbose_name=_("lesson mode"),
        help_text=_("Select in what mode lessons are offered"),
    )

    @cached_property
    def public_version(self):
        """
        Returns the latest approved version of an offer, if such a version exists.

        :return: OfferVersion or ``None``
        :rtype: ~integreat_compass.cms.models.offers.offer_version.OfferVersion
        """
        return self.versions.filter(state=True).first()

    @cached_property
    def latest_version(self):
        """
        Returns the latest version of an offer.

        :return: OfferVersion
        :rtype: ~integreat_compass.cms.models.offers.offer_version.OfferVersion
        """
        return self.versions.select_related().first()

    @cached_property
    def comments(self):
        """
        Method to retrieve all comments on an Offer.

        :return: List of comments together with information on whether the comment was made on the public offer version
        :rtype: list [ dict [ ~integreat_compass.cms.models.interactions.comment.Comment, bool ] ]
        """
        return Comment.objects.filter(offer_version__in=self.versions.all()).order_by(
            "-date"
        )

    @cached_property
    def group_type_value(self):
        """
        Helper method to get the group type for use in a template

        :return: human-readable group type
        :rtype: str
        """
        return dict(offer_group_types.CHOICES)[self.group_type]

    @cached_property
    def mode_type_value(self):
        """
        Helper method to get the mode type for use in a template

        :return: human-readable mode type
        :rtype: str
        """
        return dict(offer_mode_types.CHOICES)[self.mode_type]

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``Offer object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the page
        :rtype: str
        """
        return f"Offer {self.id}"

    def get_repr(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<Offer: Offer object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the page
        :rtype: str
        """
        return f"<Offer (id: {self.id})>"

    class Meta:
        verbose_name = _("offer")
        verbose_name_plural = _("offers")
