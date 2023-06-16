from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from ...cms.constants import offer_version_states
from ...cms.models import Vote


def determine_state(offer_version):
    """
    Returns the state of the offer version based on the votes cast on it

    :return: State of the offer version (one of :attr:`~integreat_compass.cms.constants.offer_version_states.CHOICES`)
    :rtype: str
    """
    max_votes = (
        settings.NEW_OFFER_GREMIUM_SIZE
        if offer_version.is_initial_version
        else settings.CHANGED_OFFER_GREMIUM_SIZE
    )

    if offer_version.votes.filter(approval=True).count() > max_votes // 2:
        return offer_version_states.APPROVED

    if offer_version.votes.filter(approval=False).count() > max_votes // 2:
        return offer_version_states.REJECTED

    return offer_version_states.PENDING


@receiver(post_save, sender=Vote)
def update_offer_version_state(instance, **kwargs):
    r"""
    Update the state of the offer version after voting on it.

    :param instance: The vote that gets saved
    :type instance: ~integreat_compass.cms.models.interactions.vote.Vote

    :param \**kwargs: The supplied keyword arguments
    :type \**kwargs: dict
    """
    with transaction.atomic():
        offer_version = instance.offer_version
        offer_version.state = determine_state(offer_version)
        offer_version.save()
