# Python
import datetime
import uuid

# Django
from django.core.validators import RegexValidator
from django.core.validators import ValidationError as Error
from django.db import models
from django.utils.translation import gettext as _

# Rest framework
from rest_framework.serializers import ValidationError

# Project
from taqqos.core.models import BaseDateModel

FILE_TYPES = {
    r'^(jpg|jpeg|png|gif|JPG)$': 'image',
    r'^(pdf)$': 'document',
    r'^(mp4)$': 'video'
}


def upload_name(instance, filename):
    file_type = filename.split('.')[-1]
    today = str(datetime.datetime.today())[0:7]

    for regex, folder in FILE_TYPES.items():
        try:
            RegexValidator(regex).__call__(file_type)
            return 'file/%s/%s/%s.%s' % (
                folder, today, uuid.uuid4(), file_type)
        except Error:
            pass
    raise ValidationError({
            'non_field_errors': ["File type is unacceptable"]
        })


class File(BaseDateModel):
    VIDEO = "video"
    DOCUMENT = "document"
    IMAGE = "image"
    FILE_TYPES = (
        (VIDEO, VIDEO),
        (DOCUMENT, DOCUMENT),
        (IMAGE, IMAGE)
    )
    name = models.CharField(_("название"), max_length=255, null=True, blank=True)
    file = models.FileField(_("файл"), upload_to=upload_name)
    file_type = models.CharField(_("тип файла"), max_length=30, choices=FILE_TYPES, null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to=upload_name, blank=True, null=True
    )

    class Meta:
        verbose_name = "файл"
        verbose_name_plural = "файлы"

    @property
    def file_url(self):
        return self.file.url if self.file else None
