import pytest
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase

from integreat_compass.cms.models import User, Vote
from integreat_compass.cms.views.interactions import add_vote


def get_request():
    request = RequestFactory().post("", {"approval": "False"})
    request.user = User.objects.get(pk=1)
    setattr(request, "session", "session")
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)
    return request


@pytest.mark.django_db
def test_add_vote_if_not_exists(load_test_data):
    assert Vote.objects.filter(creator=1).filter(offer_version=2).count() == 0
    request = get_request()
    add_vote(request, 2)
    assert Vote.objects.filter(creator=1).filter(offer_version=2).count() == 1
    assert not Vote.objects.filter(creator=1).filter(offer_version=2)[0].approval


@pytest.mark.django_db
def test_add_vote_if_exists(load_test_data):
    assert Vote.objects.filter(creator=1).filter(offer_version=3).count() == 1
    assert Vote.objects.filter(creator=1).filter(offer_version=3)[0].approval
    request = get_request()
    add_vote(request, 3)
    assert Vote.objects.filter(creator=1).filter(offer_version=3).count() == 1
    assert not Vote.objects.filter(creator=1).filter(offer_version=3)[0].approval
