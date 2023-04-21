*****************
Production Server
*****************

.. highlight:: bash


.. Note::

    This guide explains how to set up a production server on
    `Ubuntu 20.04.3 LTS (Focal Fossa) <https://releases.ubuntu.com/20.04/>`_. Other linux distributions should work just
    fine, but we don't provide detailed instructions for them.


System requirements
===================

    1. Upgrade alls::

        sudo apt update && sudo apt -y upgrade

    2. Install system requirements::

        sudo apt -y install python3-venv python3-pip libpq-dev ffmpeg


Integreat Compass CMS Package
=============================

    1. Choose a location for your installation, e.g. ``/opt/integreat-compass/``::

        sudo mkdir /opt/integreat-compass
        sudo chown www-data:www-data /opt/integreat-compass

    2. Create config and log files and set more restrictive permissions::

        sudo touch /var/log/integreat-compass.log /etc/integreat-compass.ini
        sudo chown www-data:www-data /var/log/integreat-compass.log /etc/integreat-compass.ini
        sudo chmod 660 /var/log/integreat-compass.log /etc/integreat-compass.ini

    3. Change to a shell with the permissions of the webserver's user ``www-data``::

        sudo -u www-data bash

    4. Create a virtual environment::

        cd /opt/integreat-compass
        python3 -m venv .venv
        source .venv/bin/activate

    5. Install the integreat-compass cms inside the virtual environment::

        pip3 install integreat-compass

       .. Note::1

           If you want to set up a test system with the latest changes from the develop branch instead of the main
           branch, use TestPyPI (with the normal PyPI repository a fallback for the dependencies)::

               pip3 install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple integreat-compass

    6. Create a symlink to the :github-source:`integreat-compass_cms/core/wsgi.py` file to facilitate the Apache configuration::

        ln -s $(python -c "from integreat-compass_cms.core import wsgi; print(wsgi.__file__)") .

    7. Set the initial configuration by adding the following to ``/etc/integreat-compass.ini`` (for a full list of all
       possible configuration values, have a look at :github-source:`example-configs/integreat-compass.ini`)::

        [integreat-compass]

        SECRET_KEY = <your-secret-key>
        FCM_KEY = <your-firebase-key>
        BASE_URL = https://cms.integreat-compass-app.de
        LOGFILE = /var/integreat-compass.log

    8. Leave the www-data shell::

        exit


Static Files
============

    1. Create root directories for all static files. It's usually good practise to separate code and data, so e.g.
       create the directory ``/var/www/integreat-compass/`` with the sub-directories ``static`` and ``media``::

        sudo mkdir -p /var/www/integreat-compass/{static,media}

    2. Make the Apache user ``www-data`` owner of these directories::

        sudo chown -R www-data:www-data /var/www/integreat-compass

    3. Add the static directories to the config in ``/etc/integreat-compass.ini``::

        STATIC_ROOT = /var/www/integreat-compass/static
        MEDIA_ROOT = /var/www/integreat-compass/media

    4. Collect static files::

        cd /opt/integreat-compass
        sudo -u www-data bash
        source .venv/bin/activate
        integreat-compass-cli collectstatic
        exit


Webserver
=========

    1. Install an `Apache2 <https://httpd.apache.org/>`_ server with `mod_wsgi <https://modwsgi.readthedocs.io/en/develop/>`_::

        sudo apt -y install apache2 libapache2-mod-wsgi-py3

    2. Enable the ``rewrite`` and ``wsgi``::

        sudo a2enmod rewrite wsgi

    3. Setup a vhost for the integreat-compass by using our example config: :github-source:`example-configs/apache2-integreat-compass-vhost.conf`
       and edit the your domain and the paths for static files.


Database
========

    1. Install a `PostgreSQL <https://www.postgresql.org/>`_ database on your system::

        sudo apt -y install postgresql

    2. Create a database user ``integreat-compass`` and set a password::

        sudo -u postgres createuser -P -d integreat-compass

    3. Create a database ``integreat-compass``::

        sudo -u postgres createdb -O integreat-compass integreat-compass

    4. Add the database credentials to the config in ``/etc/integreat-compass.ini``::

        DB_PASSWORD = <your-password>

    5. Execute initial migrations::

        cd /opt/integreat-compass
        sudo -u www-data bash
        source .venv/bin/activate
        integreat-compass-cli migrate


Email configuration
===================

    1. Add your SMTP credentials to ``/etc/integreat-compass.ini`` (for the default values, see :github-source:`example-configs/integreat-compass.ini`)::

        EMAIL_HOST = <your-smtp-server>
        EMAIL_HOST_USER = <your-username>
        EMAIL_HOST_PASSWORD = <your-password>
