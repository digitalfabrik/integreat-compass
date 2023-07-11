from django.contrib import messages
from django.db.models import Case, Count, When
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from ...constants import offer_version_states
from ...decorators import permission_required
from ...models import OfferVersion, Vote


class VoteFormView(TemplateView):
    """
    View for the vote form
    """

    template_name = "interactions/vote_form.html"

    @staticmethod
    def get_pending_offer_versions(request):
        """
        Get all offer versions that need a vote from currently logged-in user

        :param request: Object representing the user call
        :type request: ~django.http.HttpRequest

        :return: list of offer versions with all details
        """
        latest_version_of_offer = OfferVersion.objects.order_by(
            "offer", "-created_at"
        ).distinct("offer")
        offer_versions = (
            OfferVersion.objects.select_related("offer__organization")
            .prefetch_related("offer__tags", "votes")
            .annotate(
                approves=Count(Case(When(votes__approval=True, then=1))),
                declines=Count(Case(When(votes__approval=False, then=1))),
            )
            .filter(pk__in=latest_version_of_offer)
        )
        pending_offer_versions = list(
            filter(
                lambda offer_version: offer_version.state
                == offer_version_states.PENDING,
                offer_versions,
            )
        )
        for version in pending_offer_versions:
            version.user_vote = version.votes.filter(creator=request.user).first()
            version.pending = (
                version.number_of_votes_needed - version.approves - version.declines
            )
        return pending_offer_versions

    def get_context_data(self, *args, **kwargs):
        r"""
        Render :class:`~integreat_compass.cms.forms.interactions.vote_form.VoteForm`,

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :raises ~django.core.exceptions.PermissionDenied: If user does not have the permission to edit the specific page

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """
        context = super().get_context_data(**kwargs)
        pending_offer_versions: list = self.get_pending_offer_versions(self.request)
        context.update({"pending_offer_versions": pending_offer_versions})
        return context

    @require_POST
    @permission_required("vote_on_offer")
    def add_vote(self, offer_version_id):
        """
        Add vote of a user to an offer version

        :param self: Object representing the user call
        :type self: ~django.http.HttpRequest

        :param offer_version_id: internal id of the offer_version to be voted on
        :type offer_version_id: int

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """
        approval = self.POST.get("approval")
        Vote.objects.update_or_create(
            creator=self.user,
            offer_version_id=offer_version_id,
            defaults={"approval": approval},
        )
        messages.add_message(
            self,
            messages.SUCCESS,
            _('Your vote on "{}" has successfully been submitted.').format(
                OfferVersion.objects.get(id=offer_version_id).title
            ),
        )
        return redirect("/applications/votes")
