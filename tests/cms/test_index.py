import pytest
from django.test.client import Client
from django.urls import resolve, reverse


@pytest.mark.django_db
def test_offer_list_success(load_test_data):
    """
    Test if the provided list of offers is correct

    :param load_test_data: The fixture providing the test data (see :meth:`~tests.conftest.load_test_data`)
    :type load_test_data: tuple
    """
    client = Client()
    view_name = "cms:public:index"
    endpoint = reverse(view_name)
    # Check whether the endpoints resolve correctly
    match = resolve("/")
    assert match.view_name == view_name
    # Test invalid submission
    response = client.get(endpoint, {}, format="html", content_type="text/html")
    assert response.status_code == 200
    assert len(response.context["offers"]) == 3
    assert response.context["offers"][0].id == 4
    assert response.context["offers"][1].id == 5
    assert response.context["offers"][2].id == 3


@pytest.mark.django_db
def test_index_offer_tags(load_test_data):
    """
    Test if the provided list of offers is correct

    :param load_test_data: The fixture providing the test data (see :meth:`~tests.conftest.load_test_data`)
    :type load_test_data: tuple
    """
    client = Client()
    view_name = "cms:public:index"
    endpoint = reverse(view_name)
    match = resolve("/")
    assert match.view_name == view_name
    response = client.get(
        endpoint, {"tags": 4}, format="html", content_type="text/html"
    )
    assert response.status_code == 200
    assert len(response.context["offers"]) == 1
    assert response.context["offers"][0].id == 4


@pytest.mark.django_db
def test_index_multiple_offer_tags(load_test_data):
    """
    Test if the provided list of offers is correct

    :param load_test_data: The fixture providing the test data (see :meth:`~tests.conftest.load_test_data`)
    :type load_test_data: tuple
    """
    client = Client()
    view_name = "cms:public:index"
    endpoint = reverse(view_name)
    match = resolve("/")
    assert match.view_name == view_name
    response = client.get(
        endpoint, {"tags": [4, 2]}, format="html", content_type="text/html"
    )
    assert response.status_code == 200
    assert len(response.context["offers"]) == 2
    assert response.context["offers"][0].id == 4
    assert response.context["offers"][1].id == 5
