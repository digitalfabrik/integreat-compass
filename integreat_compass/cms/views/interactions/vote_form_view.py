from django.db.models import Case, Count, When
from django.shortcuts import render
from django.views.generic import TemplateView

from ...constants import offer_version_states
from ...models import OfferVersion, User


class VoteFormView(TemplateView):
    """
    View for the vote form
    """

    template_name = "interactions/vote_form.html"

    @staticmethod
    def get_pending_offer_versions(request, number_of_board_members):
        """
        Get all offer versions that need a vote from currently logged-in user

        :param request: Object representing the user call
        :type request: ~django.http.HttpRequest

        :param number_of_board_members: current number of board member
        :type number_of_board_members: int

        :return: list of offer versions with all details
        """
        latest_version_of_offer = OfferVersion.objects.order_by(
            "offer", "-created_at"
        ).distinct("offer")
        offer_versions = (
            OfferVersion.objects.prefetch_related("votes")
            .select_related("offer")
            .select_related("offer__organization")
            .prefetch_related("offer__tags")
            .annotate(approves=Count(Case(When(votes__approval=True, then=1))))
            .annotate(declines=Count(Case(When(votes__approval=False, then=1))))
            .annotate(pending=number_of_board_members - Count("votes"))
            .annotate(user_voted_on=Case(When(votes__creator=request.user, then=True)))
            .order_by("-user_voted_on")
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
        return pending_offer_versions

    def get(self, request, *args, **kwargs):
        number_of_board_members = User.objects.filter(
            groups__name="BOARD_MEMBER"
        ).count()
        pending_offer_versions: list = self.get_pending_offer_versions(
            request, number_of_board_members
        )
        return render(
            request,
            self.template_name,
            {
                **self.get_context_data(**kwargs),
                "pending_offer_versions": pending_offer_versions,
                "number_of_board_members": number_of_board_members,
            },
        )
