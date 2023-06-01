import pytest
from django.contrib import auth
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    "email", ["root@integreat.compass", "offer_provider@integreat.compass"]
)
def test_login_success(load_test_data, client, settings, email):
    """
    Test whether login via username & email works as expected

    :param load_test_data: The fixture providing the test data (see :meth:`~tests.conftest.load_test_data`)
    :type load_test_data: tuple

    :param client: The fixture providing the an unauthenticated user client
    :type client: :fixture:`client`

    :param settings: The Django settings
    :type settings: :fixture:`settings`

    :param email: The email to use for login
    :type email: str
    """
    response = client.post(
        reverse(settings.LOGIN_URL), data={"username": email, "password": "compass"}
    )
    print(response.headers)
    assert response.status_code == 302
    response = client.get(reverse(settings.LOGIN_REDIRECT_URL))
    user = auth.get_user(client)
    assert user.is_authenticated


@pytest.mark.django_db
@pytest.mark.parametrize(
    "email", ["root", "root@integreat.compass", "non-existing-email@example.com", ""]
)
def test_login_failure(load_test_data, client, settings, email):
    """
    Test whether login with incorrect credentials does not work

    :param load_test_data: The fixture providing the test data (see :meth:`~tests.conftest.load_test_data`)
    :type load_test_data: tuple

    :param client: The fixture providing the an unauthenticated user client
    :type client: :fixture:`client`

    :param settings: The Django settings
    :type settings: :fixture:`settings`

    :param email: The email to use for login
    :type email: str
    """
    settings.LANGUAGE_CODE = "en"
    response = client.post(
        reverse(settings.LOGIN_URL), data={"username": email, "password": "incorrect"}
    )
    print(response.headers)
    assert response.status_code == 200
    assert "The username or the password is incorrect." in response.content.decode()
