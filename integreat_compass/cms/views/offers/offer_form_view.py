import logging

from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from ...decorators import permission_required
from ...forms import (
    ContactForm,
    DocumentUploadForm,
    LocationForm,
    OfferForm,
    OfferVersionForm,
    OrganizationForm,
)
from ...models import Offer

logger = logging.getLogger(__name__)


@method_decorator(permission_required("cms.change_offer"), name="dispatch")
class OfferFormView(TemplateView):
    """
    View for the offer form
    """

    template_name = "offers/offer_form.html"

    @staticmethod
    def _get_forms(offer_id, **kwargs):
        if offer_id:
            offer = Offer.objects.get(id=offer_id)
            offer_version = offer.versions.first()
            offer_contact = offer.offer_contact
            offer_location = offer.location
            offer_organization = offer.organization
        else:
            offer = offer_version = offer_contact = offer_location = offer_organization = None  # fmt: skip

        offer_form = OfferForm(instance=offer, **kwargs)
        offer_version_form = OfferVersionForm(instance=offer_version, **kwargs)
        contact_form = ContactForm(instance=offer_contact, **kwargs)
        location_form = LocationForm(instance=offer_location, **kwargs)
        organization_form = OrganizationForm(instance=offer_organization, **kwargs)

        return {
            "offer_form": offer_form,
            "offer_version_form": offer_version_form,
            "contact_form": contact_form,
            "location_form": location_form,
            "organization_form": organization_form,
        }

    def get(self, request, *args, **kwargs):
        r"""
        Render :class:`~integreat_compass.cms.forms.offers.contact_form.ContactForm`,
               :class:`~integreat_compass.cms.forms.offers.location_form.LocationForm`,
               :class:`~integreat_compass.cms.forms.offers.offer_form.OfferForm`,
               :class:`~integreat_compass.cms.forms.offers.offer_version_form.OfferVersionForm` and
               :class:`~integreat_compass.cms.forms.offers.organization_form.OrganizationForm`

        :param request: The current request
        :type request: ~django.http.HttpRequest

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :raises ~django.core.exceptions.PermissionDenied: If user does not have the permission to edit the specific page

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """

        return render(
            request,
            self.template_name,
            {**self._get_forms(kwargs.get("pk")), **self.get_context_data(**kwargs)},
        )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        r"""
        Submit :class:`~integreat_compass.cms.forms.offers.contact_form.ContactForm`,
               :class:`~integreat_compass.cms.forms.offers.location_form.LocationForm`,
               :class:`~integreat_compass.cms.forms.offers.offer_form.OfferForm`,
               :class:`~integreat_compass.cms.forms.offers.offer_version_form.OfferVersionForm` and
               :class:`~integreat_compass.cms.forms.offers.organization_form.OrganizationForm`

        :param request: The current request
        :type request: ~django.http.HttpRequest

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :raises ~django.core.exceptions.PermissionDenied: If user does not have the permission to edit the specific page

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """
        forms = self._get_forms(
            kwargs.get("pk"),
            data=request.POST,
            files=request.FILES,
            additional_instance_attributes={"creator": request.user},
        )

        new_document_forms = [
            DocumentUploadForm(instance=None, data=request.POST, initial={"file": file})
            for file in request.FILES.getlist("document-upload-zone")
        ]

        if not all(form.is_valid() for form in [*forms.values(), *new_document_forms]):
            for form in [*forms.values(), *new_document_forms]:
                form.add_error_messages(request)

            return render(
                request,
                self.template_name,
                {**forms, **self.get_context_data(**kwargs)},
            )

        (
            offer_form,
            offer_version_form,
            contact_form,
            location_form,
            organization_form,
        ) = forms.values()

        offer_form.instance.offer_contact = contact_form.save()
        offer_form.instance.location = location_form.save()
        offer_form.instance.organization = organization_form.save()

        offer_version_form.instance.offer = offer_form.save()
        offer_version_instance = offer_version_form.save()

        for document_form in new_document_forms:
            document = document_form.save()
            document.offer_versions.add(offer_version_instance)
            document.save()

        messages.success(
            request,
            _(
                'Application for the offer "{}" has successfully been submitted and will be reviewed shortly.'
            ).format(offer_version_instance.title),
        )
        return redirect("cms:protected:edit_offer", **{"pk": offer_form.instance.id})
