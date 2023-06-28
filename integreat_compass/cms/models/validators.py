from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _


def file_size_limit(value):
    """
    This function checks if the uploaded file exceeds the file size limit

    :param value: the size of upload file
    :type value: int

    :raises ~django.core.exceptions.ValidationError: when the file size exceeds the size given in the settings.

    """
    if value.size > settings.MEDIA_MAX_UPLOAD_SIZE:
        raise ValidationError(
            _("File too large. Size should not exceed {}.").format(
                filesizeformat(settings.MEDIA_MAX_UPLOAD_SIZE)
            )
        )
