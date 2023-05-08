"""
Django URL dispatcher for the cms package.
See :mod:`~integreat_compass.core.urls` for the other namespaces of this application.

For more information on this file, see :doc:`django:topics/http/urls`.
"""

from django.urls import include, path

from ..constants import namespaces

#: The namespace for this URL config (see :attr:`django.urls.ResolverMatch.app_name`)
app_name = "cms"

#: The url patterns of this module (see :doc:`django:topics/http/urls`)
urlpatterns = [
    path(
        "",
        include(
            ("integreat_compass.cms.urls.public", app_name), namespace=namespaces.PUBLIC
        ),
    ),
    path(
        "",
        include(
            ("integreat_compass.cms.urls.protected", app_name),
            namespace=namespaces.PROTECTED,
        ),
    ),
]
