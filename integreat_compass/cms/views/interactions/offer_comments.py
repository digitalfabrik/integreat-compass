"""
This module provides the commenting action.
"""
import logging

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from ...models import Comment, Offer

logger = logging.getLogger(__name__)


@require_POST
def add_comment(request):
    """
    Add a comment to an offer

    :param request: The current request
    :type request: ~django.http.HttpRequest

    :raises ~django.core.exceptions.PermissionDenied: If user does not have the permission to edit the specific page

    :return: An HTTP status code
    :rtype: ~django.http.HttpResponse
    """
    if not request.user.has_perm("cms.add_comment"):
        raise PermissionDenied(
            f"{request.user!r} does not have the permission to add a comment."
        )

    comment, offer_id = request.POST.get("comment"), request.POST.get("offer_id")
    if (
        not comment
        or not (offer := Offer.objects.filter(pk=offer_id).first())
        or len(comment) > settings.MAX_COMMENT_LENGTH
    ):
        return HttpResponse(status=400)

    comment_object = Comment.objects.create(
        creator=request.user, offer_version=offer.public_version, comment=comment
    )
    logger.debug("Created new comment: %r", comment_object)
    return HttpResponse(status=201)
