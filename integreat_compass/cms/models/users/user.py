from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    PermissionsMixin,
)
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ...constants import group_names
from ..abstract_base_model import AbstractBaseModel


class CustomUserManager(BaseUserManager):
    """
    This manager provides custom methods for user creation
    """

    def create_user(
        self, email, display_name, password=None, group=None, **extra_fields
    ):
        """
        Create a new user and ensure they are added to the correct group (if any)

        :param email: email address of the user, also used in lieu of username
        :type email: str

        :param display_name: name used for comments etc.
        :type display_name: str

        :param password: user password
        :type password: str

        :param group: either None or one of :attr:`~integreat_compass.cms.constants.group_names.CHOICES`
        :type group: str

        :param extra_fields: additional fields
        :type extra_fields: dict

        :return: the newly created user
        :rtype: ~integreat_compass.cms.models.users.user.User
        """
        email = self.normalize_email(email)
        user = self.model(email=email, display_name=display_name, **extra_fields)

        if group and group in group_names.CHOICES:
            user.groups.add(Group.objects.get(name=group))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, display_name, password=None, **extra_fields):
        """
        Create a new super user

        :param email: email address of the user, also used in lieu of username
        :type email: str

        :param display_name: name used for comments etc.
        :type display_name: str

        :param password: user password
        :type password: str

        :param extra_fields: additional fields
        :type extra_fields: dict

        :return: the newly created user
        :rtype: ~integreat_compass.cms.models.users.user.User
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, display_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """
    A custom User model that replaces the default Django User model.
    """

    email = models.EmailField(
        unique=True,
        verbose_name=_("email"),
        help_text=_("Valid email address for this user"),
    )
    display_name = models.CharField(
        max_length=128,
        verbose_name=_("display name"),
        help_text=_("This name will be shown as the author of votes, comments, etc."),
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["display_name"]

    @cached_property
    def group(self):
        """
        Return the primary group of this user

        :return: The first group of this user
        :rtype: ~django.contrib.auth.models.Group
        """
        return self.groups.first()

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``User object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the user
        :rtype: str
        """
        return f"{self.display_name} ({self.email})"

    def get_repr(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<User: User object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the user
        :rtype: str
        """
        fields = [
            f"id: {self.id}",
            f"email: {self.email}",
            f"display_name: {self.display_name}",
            f"group: {self.groups.first()}",
            f"is_staff: {self.is_staff}",
        ]
        return f"<User ({', '.join(fields)})>"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["email"]
        default_permissions = ("change", "delete", "view")
