import logging

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    """
    This class represents the Django-configuration of the backend.

    See :class:`django.apps.AppConfig` for more information.

    :param name: The name of the app
    :type name: str
    """

    name = "integreat_compass.core"
    verbose_name = _("Core")

    def ready(self):
        # pylint: disable=unused-import,import-outside-toplevel
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals
