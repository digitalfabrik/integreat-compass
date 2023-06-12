import pytest
from django.test import RequestFactory, TestCase

from integreat_compass.cms.models import User, Vote
from integreat_compass.cms.views.interactions import add_vote


@pytest.mark.django_db
def test_add_vote_if_not_exists(load_test_data):
    assert Vote.objects.filter(creator=1).filter(offer_version=2).count() == 0
    request = RequestFactory().post("", {"approval": "False"})
    request.user = User.objects.get(pk=1)
    add_vote(request, 2)
    assert Vote.objects.filter(creator=1).filter(offer_version=2).count() == 1
    assert Vote.objects.filter(creator=1).filter(offer_version=2)[0].approval == False


@pytest.mark.django_db
def test_add_vote_if_exists(load_test_data):
    assert Vote.objects.filter(creator=1).filter(offer_version=1).count() == 1
    assert Vote.objects.filter(creator=1).filter(offer_version=1)[0].approval == True
    request = RequestFactory().post("", {"approval": "False"})
    request.user = User.objects.get(pk=1)
    add_vote(request, 1)
    assert Vote.objects.filter(creator=1).filter(offer_version=1).count() == 1
    assert Vote.objects.filter(creator=1).filter(offer_version=1)[0].approval == False
