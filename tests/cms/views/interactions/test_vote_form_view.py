import pytest
from django.test import RequestFactory, TestCase

from integreat_compass.cms.models import OfferVersion, User, Vote
from integreat_compass.cms.views.interactions import add_vote, VoteFormView


@pytest.mark.django_db
def test_display_only_newest_offer_version(load_test_data):
    number_of_board_members = User.objects.filter(groups__name="BOARD_MEMBER").count()
    request = RequestFactory().get("")
    request.user = User.objects.get(pk=1)
    assert OfferVersion.objects.all().count() == 3
    assert number_of_board_members == 4
    pending_offer_versions = VoteFormView.get_pending_offer_versions(request, 4)
    assert len(pending_offer_versions) == 2
    assert any(
        offer_version.title
        == "Fortgeschrittenes Deutsch - Konversationskurs für die Arbeitswelt - überarbeitet"
        for offer_version in pending_offer_versions
    )
    assert not any(
        offer_version.title
        == "Fortgeschrittenes Deutsch - Konversationskurs für die Arbeitswelt"
        for offer_version in pending_offer_versions
    )
