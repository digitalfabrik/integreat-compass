from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CmsConfig(AppConfig):
    """
    This class represents the Django-configuration of the CMS.

    See :class:`django.apps.AppConfig` for more information.

    :param name: The name of the app
    :type name: str
    """

    name = "integreat_compass.cms"
    verbose_name = _("CMS")

    def ready(self):
        # pylint: disable-next=import-outside-toplevel
        from django.contrib.auth.models import Group

        Group.__str__ = lambda self: self.name
