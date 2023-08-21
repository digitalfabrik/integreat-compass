from django.contrib import messages
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from ...decorators import permission_required
from ...models import OfferVersion, Report


@method_decorator(permission_required("cms.add_vote"), name="dispatch")
class ReportListView(TemplateView):
    """
    View for the report list
    """

    template_name = "components/report_list.html"

    def get_context_data(self, **kwargs):
        r"""
        Context for the report list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """
        return super().get_context_data(**kwargs) | {"reports": Report.objects.all()}

    def post(self, request, *args, **kwargs):
        r"""
        Handle form to declare a reported offer as declined

        :param request: The current requestHttpResponseRedirect
        :type request: ~django.http.HttpRequest

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.HttpResponseRedirect

        """
        offer_version_id = request.POST.get("offer_version_id")
        if request.POST.get("move-to-declined"):
            OfferVersion.objects.filter(id=offer_version_id).update(state="False")

        messages.success(
            request,
            _('You rejected the reported offer "{}"').format(
                OfferVersion.objects.get(id=offer_version_id).title
            ),
        )
        return redirect("cms:protected:reports")
