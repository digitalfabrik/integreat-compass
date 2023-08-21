from django.views.generic import TemplateView

from ...models import OfferVersion


class DeclineListView(TemplateView):
    """
    View for the decline list
    """

    template_name = "interactions/decline_list.html"

    def get_context_data(self, **kwargs):
        r"""
        Context for the list of declined offers

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """
        return super().get_context_data(**kwargs) | {
            "declined_offers": OfferVersion.objects.filter(state="False").distinct(
                "offer"
            )
        }
