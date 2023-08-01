"""
This module contains shared fixtures for pytest
"""
import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test.client import Client

ROOT = "root@integreat.compass"
BOARD_MEMBER = "board_member@integreat.compass"
INTEGRATION_SPECIALIST = "integration_specialist@integreat.compass"
OFFER_PROVIDER = "offer_provider@integreat.compass"
ANONYMOUS = "ANONYMOUS"

ROLES = [ROOT, BOARD_MEMBER, INTEGRATION_SPECIALIST, OFFER_PROVIDER]
ALL_ROLES = ROLES + [ANONYMOUS]


@pytest.fixture(scope="session")
def load_test_data(django_db_setup, django_db_blocker):
    """
    Load the test data initially for all test cases

    :param django_db_setup: The fixture providing the database availability
    :type django_db_setup: :fixture:`django_db_setup`

    :param django_db_blocker: The fixture providing the database blocker
    :type django_db_blocker: :fixture:`django_db_blocker`
    """
    with django_db_blocker.unblock():
        call_command("loaddata", "integreat_compass/cms/fixtures/test_data.json")


@pytest.fixture(scope="function")
def load_test_data_transactional(transactional_db, django_db_blocker):
    """
    Load the test data initially for all transactional test cases

    :param transactional_db: The fixture providing transaction support for the database
    :type transactional_db: :fixture:`transactional_db`

    :param django_db_blocker: The fixture providing the database blocker
    :type django_db_blocker: :fixture:`django_db_blocker`
    """
    with django_db_blocker.unblock():
        call_command("loaddata", "integreat_compass/cms/fixtures/test_data.json")
        call_command("loaddata", "integreat_compass/cms/fixtures/permissions.json")


# pylint: disable=redefined-outer-name
@pytest.fixture(scope="session", params=ALL_ROLES)
def login_role_user(request, load_test_data, django_db_blocker):
    """
    Get the test user of the current role and force a login. Gets executed only once per user.

    :param request: The request object providing the parametrized role variable through ``request.param``
    :type request: pytest.FixtureRequest

    :param load_test_data: The fixture providing the test data (see :meth:`~tests.conftest.load_test_data`)
    :type load_test_data: NoneType

    :param django_db_blocker: The fixture providing the database blocker
    :type django_db_blocker: :fixture:`django_db_blocker`

    :return: The http client and the current role
    :rtype: tuple
    """
    client = Client()
    # Only log in user if the role is not anonymous
    if request.param != ANONYMOUS:
        with django_db_blocker.unblock():
            print(request.param.lower())
            user = get_user_model().objects.get(email=request.param.lower())
            client.force_login(user)
    return client, request.param
