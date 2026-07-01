"""
Shared configuration loading for the Integreat Compass entry points (CLI and WSGI).
"""

import configparser
import os


def read_config_file():
    """
    Set the default Django settings module and load the configuration from
    ``/etc/integreat-compass.ini`` into the environment.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "integreat_compass.core.settings")

    # Read config from config file
    config = configparser.ConfigParser(interpolation=None)
    config.read("/etc/integreat-compass.ini")
    for section in config.sections():
        for key, value in config.items(section):
            os.environ.setdefault(f"INTEGREAT_COMPASS_{key.upper()}", value)
