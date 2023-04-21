*****************
Development Tools
*****************

This is a collection of scripts which facilitate the development process.
They are targeted at as much platforms and configurations as possible, but there might be edge cases in which they don’t work as expected.

Installation
============

Install all project dependencies and the local python package with :github-source:`tools/install.sh`::

    ./tools/install.sh [--clean] [--pre-commit] [--python PYTHON_VERSION]

* ``--clean``: Remove all installed dependencies in the ``.venv/`` and ``node_modules/`` directories as well as compiled
  static files in ``integreat_compass/static/dist/``.
* ``--pre-commit``: Install all :ref:`pre-commit-hooks`
* ``--python``: Use the specified ``PYTHON_VERSION`` (e.g. ``python3.9``) if your system's default version differs from ``3.9``

Development Server
==================

Run the inbuilt local webserver with :github-source:`tools/run.sh`::

    ./tools/run.sh [--fast]

**Options:**

* ``--fast``: Skip migrations and translation on startup and just start Django

Test Data
=========

Import test data into the database :github-source:`tools/loadtestdata.sh`::

    ./tools/loadtestdata.sh

Documentation
=============

Build this documentation with :github-source:`tools/make_docs.sh`::

    ./tools/make_docs.sh [--clean]

**Options:**

* ``--clean``: Remove all temporary documentation files in the ``docs/src/ref/`` directory
  as well as the compiled html output in ``docs/dist``. Existing outdated documentation files can cause the
  generation script to fail if e.g. source files were added or deleted.
