import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from ...decorators import permission_required
from ...forms import (
    ContactForm,
    LocationForm,
    OfferForm,
    OfferVersionForm,
    OrganizationForm,
)
from ...models import Offer, User

logger = logging.getLogger(__name__)


@method_decorator(permission_required("cms.edit_offer"), name="dispatch")
class OfferFormView(TemplateView):
    """
    View for the offer form
    """

    template_name = "offers/offer_form.html"

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

        offer = Offer.objects.filter(id=kwargs.get("offer_id")).first()
        (offer_version, offer_contact, offer_location, offer_organization) = (
            (
                offer.versions.latest(),
                offer.offer_contact,
                offer.location,
                offer.organization,
            )
            if offer is not None
            else (None, None, None, None)
        )
        offer_form = OfferForm(instance=offer)
        offer_version_form = OfferVersionForm(instance=offer_version)
        contact_form = ContactForm(instance=offer_contact)
        location_form = LocationForm(instance=offer_location)
        organization_form = OrganizationForm(instance=offer_organization)

        return render(
            request,
            self.template_name,
            {
                **self.get_context_data(**kwargs),
                "offer_form": offer_form,
                "offer_version_form": offer_version_form,
                "contact_form": contact_form,
                "location_form": location_form,
                "organization_form": organization_form,
            },
        )

    # pylint: disable=too-many-locals
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
        offer_instance = Offer.objects.filter(id=kwargs.get("offer_id")).first()
        if not request.user.has_perm("cms.edit_offer", offer_instance):
            raise PermissionDenied(
                f"{request.user!r} does not have the permission to edit {offer_instance!r}"
            )

        user = User.objects.get(pk=request.user.id)

        offer_form = OfferForm(
            data=request.POST, additional_instance_attributes={"user": user}
        )
        offer_version_form = OfferVersionForm(
            data=request.POST, additional_instance_attributes={"user": user}
        )
        contact_form = ContactForm(
            data=request.POST, additional_instance_attributes={"user": user}
        )
        location_form = LocationForm(
            data=request.POST, additional_instance_attributes={"user": user}
        )
        organization_form = OrganizationForm(
            data=request.POST, additional_instance_attributes={"user": user}
        )

        forms = (
            offer_form,
            offer_version_form,
            contact_form,
            location_form,
            organization_form,
        )
        if not all(form.is_valid() for form in forms):
            for form in forms:
                form.add_error_messages(request)
        else:
            print(contact_form.is_valid())
            contact_instance = contact_form.save()
            location_instance = location_form.save()
            organization_instance = organization_form.save()

            offer_instance = offer_form.save(commit=False)
            offer_instance.offer_contact = contact_instance
            offer_instance.location = location_instance
            offer_instance.organization = organization_instance
            offer_instance.save()
            offer_form.save_m2m()

            offer_version_instance = offer_version_form.save(commit=False)
            offer_version_instance.offer = offer_instance
            offer_version_instance.save()

            messages.success(
                request,
                _(
                    'Application for the offer "{}" has successfully been submitted and will be reviewed shortly.'
                ).format(offer_version_instance.title),
            )

        return render(
            request,
            self.template_name,
            {
                **self.get_context_data(**kwargs),
                "offer_form": offer_form,
                "offer_version_form": offer_version_form,
                "contact_form": contact_form,
                "location_form": location_form,
                "organization_form": organization_form,
            },
        )
