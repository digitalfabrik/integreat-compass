from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from ...decorators import permission_required
from ...models import Vote


@require_POST
@permission_required("vote_on_offer")
def add_vote(request, offer_version_id):
    """
    Add vote of a user to an offer version

    :param request: Object representing the user call
    :type request: ~django.http.HttpRequest

    :param offer_version_id: internal id of the offer_version to be voted on
    :type offer_version_id: int

    :return: The rendered template response
    :rtype: ~django.template.response.TemplateResponse
    """
    approval = request.POST.get("approval")
    vote = Vote.objects.filter(creator=request.user).filter(
        offer_version=offer_version_id
    )
    if vote:
        vote[0].approval = approval
        vote[0].save()
    else:
        new_vote = Vote(
            creator=request.user, offer_version_id=offer_version_id, approval=approval
        )
        new_vote.save()
    return redirect("/dashboard/votes")
