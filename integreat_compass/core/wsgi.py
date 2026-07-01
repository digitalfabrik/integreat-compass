"""
WSGI config for integreat_compass project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from .config import read_config_file


def application(environ, start_response):
    """
    This returns the WSGI callable

    :param environ: The environment variables
    :type environ: dict

    :param start_response: A function which starts the response
    :type start_response: ~collections.abc.Callable

    :return: The WSGI callable
    :rtype: ~django.core.handlers.WSGIHandler
    """
    read_config_file()

    # Read config from environment
    for key in environ:
        if key.startswith("INTEGREAT_COMPASS_"):
            os.environ[key] = environ[key]

    _application = get_wsgi_application()

    return _application(environ, start_response)
