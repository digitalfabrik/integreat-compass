import logging

from django import forms
from django.contrib import messages
from django.core.exceptions import FieldDoesNotExist
from django.utils import translation
from django.utils.functional import keep_lazy_text
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _


@keep_lazy_text
def lowfirst(string):
    """
    Make the first letter of a string lowercase (counterpart of :func:`~django.utils.text.capfirst`, see also
    :templatefilter:`capfirst`).

    :param string: The input text
    :type string: str

    :return: The lowercase text
    :rtype: str
    """
    return string and str(string)[0].lower() + str(string)[1:]


class CustomModelForm(forms.ModelForm):
    """
    Form for populating all text widgets of a ModelForm with the default placeholder "Enter ... here".
    Use this form as base class instead of :class:`django.forms.ModelForm`.
    """

    def _add_instance_attributes(self, attributes):
        for name, value in attributes.items():
            setattr(self.instance, name, value)

    def _setup_logging(self):
        self.logger = logging.getLogger(type(self).__module__)

        attributes = []
        if self.data:
            attributes.append("data")
        if self.files:
            attributes.append("files")
        if self.initial:
            attributes.append("initial")
        if self.instance.id:
            attributes.append("instance")

        self.logger.debug(
            "%s initialized"
            + (" with " + ": %r, ".join(attributes) + ": %r" if attributes else ""),
            type(self).__name__,
            *[getattr(self, attribute) for attribute in attributes],
        )

    def _init_fields(self, disabled):
        for field_name, field in self.fields.items():
            field.disabled = disabled

            if isinstance(
                field.widget,
                (
                    forms.TextInput,
                    forms.Textarea,
                    forms.EmailInput,
                    forms.URLInput,
                    forms.PasswordInput,
                    forms.NumberInput,
                ),
            ):
                try:
                    # Use verbose_name of model field instead of field label because label is capitalized
                    model_field = self._meta.model._meta.get_field(
                        field_name
                    ).verbose_name
                except FieldDoesNotExist:
                    model_field = lowfirst(field.label)

                field.widget.attrs.update(
                    {"placeholder": capfirst(_("Enter {} here").format(model_field))}
                )

    def __init__(self, **kwargs):
        r"""
        Initialize placeholder model form

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :raises TypeError: If form is instantiated directly without an inheriting subclass
        """
        # pop kwargs to make sure the super class does not get these params
        disabled = kwargs.pop("disabled", False)
        additional_instance_attributes = kwargs.pop(
            "additional_instance_attributes", {}
        )

        try:
            super().__init__(**kwargs)
        except ValueError as e:
            raise TypeError("CustomModelForm cannot be instantiated directly.") from e

        self._add_instance_attributes(additional_instance_attributes)
        self._setup_logging()
        self._init_fields(disabled)

    def clean(self):
        """
        This method extends the default ``clean()``-method of the base :class:`~django.forms.ModelForm` to provide debug
        logging

        :return: The cleaned data (see :ref:`overriding-modelform-clean-method`)
        :rtype: dict
        """
        cleaned_data = super().clean()
        self.logger.debug(
            "%s validated with cleaned data %r", type(self).__name__, cleaned_data
        )
        return cleaned_data

    def save(self, commit=True):
        """
        This method extends the default ``save()``-method of the base :class:`~django.forms.ModelForm`
        to provide debug logging

        :param commit: Whether or not the changes should be written to the database
        :type commit: bool

        :return: The saved object returned by :ref:`django:topics-modelform-save`
        :rtype: object
        """
        self.logger.debug(
            "%s saved with changed data %r", type(self).__name__, self.changed_data
        )

        return super().save(commit=commit)

    def add_error_messages(self, request):
        """
        This function accepts the current request and adds the form's error messages to the message queue of
        :mod:`django.contrib.messages`.

        :param request: The current request submitting the form
        :type request: ~django.http.HttpRequest
        """
        for field in self:
            for error in field.errors:
                messages.error(request, _(field.label) + ": " + _(error))

        for error in self.non_field_errors():
            messages.error(request, _(error))

        with translation.override("en"):
            self.logger.debug(
                "%r submitted with errors: %r", type(self).__name__, self.errors
            )

    def get_error_messages(self):
        """
        Return all error messages of this form and append labels to errors

        :return: The errors of this form
        :rtype: list
        """
        error_messages = []

        for field in self:
            for error in field.errors:
                error_messages.append(
                    {"type": "error", "text": field.label + ": " + error}
                )

        for error in self.non_field_errors():
            error_messages.append({"type": "error", "text": error})
        return error_messages
