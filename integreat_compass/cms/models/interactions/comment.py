from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..abstract_base_model import AbstractBaseModel
from ..offers.offer_version import OfferVersion
from ..users.user import User


class Comment(AbstractBaseModel):
    """
    Data model representing a Comment.
    """

    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    offer_version = models.ForeignKey(OfferVersion, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(
        verbose_name=_("comment"),
        help_text=_("Additional context for the given rating"),
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("rating"),
        help_text=_("Rating of the offer"),
    )

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``Comment object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the page
        :rtype: str
        """
        return f"Comment on {self.offer_version}"

    def get_repr(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<Comment: Comment object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the page
        :rtype: str
        """
        return f"<Comment (id: {self.id}, user: {self.creator}, offer_version: {self.offer_version})>"

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        default_related_name = "comments"
        ordering = ["date"]
        default_permissions = ("change", "delete", "view")
        permissions = [("comment_on_offer", "can add a comment to an offer")]
