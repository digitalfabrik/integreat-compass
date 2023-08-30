import pytest
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory

from integreat_compass.cms.models import User, Vote
from integreat_compass.cms.views.interactions import VoteFormView


def get_request(offer_version_id):
    request = RequestFactory().post(
        "",
        {"approval": "False", "offer_version_id": offer_version_id, "reason": "reason"},
    )
    request.user = User.objects.get(pk=1)
    setattr(request, "session", "session")
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)
    return request


@pytest.mark.django_db
def test_add_vote_if_not_exists(load_test_data):
    assert not Vote.objects.filter(creator=1, offer_version=2).exists()
    request = get_request(2)
    VoteFormView.as_view()(request)
    assert not Vote.objects.get(creator=1, offer_version=2).approval


@pytest.mark.django_db
def test_add_vote_if_exists(load_test_data):
    assert Vote.objects.get(creator=1, offer_version=3).approval
    request = get_request(3)
    VoteFormView.as_view()(request)
    assert not Vote.objects.get(creator=1, offer_version=3).approval
