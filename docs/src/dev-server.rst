******************
Development Server
******************

Run the inbuilt local webserver with :github-source:`tools/run.sh`::

    ./tools/run.sh

This is a convenience script which also performs the following actions:

* Activate the virtual environment
* Migrate database
* Import test data on first start
* Regenerate and compile translation file

If you want to speed up this process and don't need the extra functionality, you might also use::

    ./tools/run.sh --fast

After that, open your browser and navigate to http://localhost:8082/. By default, the following users exist:

========================================  ========================
Email                                     Group
========================================  ========================
root@integreat.compass                    \-
board_member@integreat.compass            BOARD_MEMBER
integration_specialist@integreat.compass  INTEGRATION_SPECIALIST
offer_provider@integreat.compass          OFFER_PROVIDER
========================================  ========================

All default users share the password `compass`.

.. Note::

    If you want to use another port than ``8082``, edit :github-source:`tools/utils/_functions.sh`.
