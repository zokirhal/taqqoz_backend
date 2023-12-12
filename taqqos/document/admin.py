import re
from typing import Any

from django.contrib import admin
from django.db import transaction
from django.utils.safestring import mark_safe

from taqqos.document.models import File, FILE_TYPES
from taqqos.document.services import create_video_preview, create_thumbnail_image


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "file_type", "file", "file_tag"]
    list_filter = ["file_type", 'created_at']
    readonly_fields = ["thumbnail", "file_type"]

    def file_tag(self, obj: File) -> Any:
        if obj.file:
            return mark_safe(
                '<img src="{}" height="50"/>'.format(obj.thumbnail.url)
            )
        return None

    file_tag.short_description = "краткий изображение"

    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            super().save_model(request, obj, form, change)
            thumb_extension = str(obj.file.name).split(".")[-1]
            file_type = None
            for key, val in FILE_TYPES.items():
                if re.match(key, thumb_extension):
                    file_type = val
                    break
            obj.file_type = file_type
            obj.save()
            match file_type:
                case File.VIDEO:
                    create_video_preview(obj)
                case File.IMAGE:
                    create_thumbnail_image(obj)
