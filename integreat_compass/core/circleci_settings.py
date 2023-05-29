"""
Django settings for our CircleCI workflow.
All configurations are imported from :mod:`~integreat_compass.core.settings`.
For more information on this file, see :doc:`django:topics/settings`.
For the full list of settings and their values, see :doc:`django:ref/settings`.
"""
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from .settings import *

#: Set a dummy secret key for CircleCI build even if it's not in debug mode
SECRET_KEY = "dummy"
LOG_LEVEL = "DEBUG"
