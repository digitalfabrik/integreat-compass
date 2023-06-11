import logging
import mimetypes
from os.path import splitext

import magic
from django import forms
from django.utils.translation import gettext_lazy as _

from ...constants import allowed_media
from ...models import Document
from ..custom_model_form import CustomModelForm

logger = logging.getLogger(__name__)


class DocumentUploadForm(CustomModelForm):
    """
    Form for uploading documents
    """

    prefix = "document_upload"

    class Meta:
        model = Document
        fields = ["file", "name", "file_type", "file_size"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = False
        self.fields["file_type"].required = False
        self.fields["file_size"].required = False

    def clean(self):
        """
        Validate form fields which depend on each other, see :meth:`django.forms.Form.clean`:
        If the file type is invalid, add a :class:`~django.core.exceptions.ValidationError`.

        :return: The cleaned form data
        :rtype: dict
        """
        cleaned_data = super().clean()
        if not (file := cleaned_data.get("file")):
            return cleaned_data

        file_type = magic.from_buffer(file.read(), mime=True)
        if file_type not in dict(allowed_media.CHOICES):
            self.add_error(
                "file_type",
                forms.ValidationError(
                    _("The file type {} is not allowed.").format(file_type)
                    + " "
                    + _("Allowed file types")
                    + ": "
                    + ", ".join(map(str, dict(allowed_media.CHOICES).values())),
                    code="invalid",
                ),
            )

        name, extension = splitext(file.name)
        valid_extensions = mimetypes.guess_all_extensions(file_type)
        if valid_extensions and extension not in valid_extensions:
            extension = valid_extensions[0]

        cleaned_data["file"] = file
        cleaned_data["name"] = name + extension
        cleaned_data["file_type"] = file_type
        cleaned_data["file_size"] = file.size

        return cleaned_data
