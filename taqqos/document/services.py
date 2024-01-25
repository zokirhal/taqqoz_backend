import io
import os

from django.core.files.base import ContentFile
from moviepy.editor import VideoFileClip
from PIL import Image

from taqqos.core import serializers
from taqqos.document.models import File


def create_video_preview(instance: File):
    path = instance.file.path
    try:
        video = VideoFileClip(path)
    except Exception as e:
        raise serializers.ValidationError({
            'file': ['Not video.']
        })
    if video.duration > 1200:
        raise serializers.ValidationError({
            'file': ['Max duration 120s.']
        })

    frame = video.get_frame(1)
    image = Image.fromarray(frame)

    data = io.BytesIO()
    image.save(data, 'JPEG')
    data.seek(0)

    file = data.getvalue()
    instance.thumbnail.save('preview.jpeg', ContentFile(file))


def create_thumbnail_image(instance, size=(300, 300)):
    image = Image.open(instance.file)
    image.thumbnail(size, Image.ANTIALIAS)
    thumb_name, thumb_extension = os.path.splitext(instance.file.name)
    thumb_extension = thumb_extension.lower()

    thumb_filename = (
        thumb_name + f"_thumb_{size[0]}_{size[1]}" + thumb_extension
    )

    if thumb_extension in [".jpg", ".jpeg", ".JPG"]:
        FTYPE = "JPEG"
    elif thumb_extension == ".gif":
        FTYPE = "GIF"
    elif thumb_extension == ".png":
        FTYPE = "PNG"
    elif thumb_extension in [".webp", ".WEBP"]:
        FTYPE = "WEBP"

    temp_thumb = io.BytesIO()
    image.save(temp_thumb, FTYPE)
    temp_thumb.seek(0)

    instance.thumbnail.save(
        thumb_filename, ContentFile(temp_thumb.read()), save=False
    )
    temp_thumb.close()
    instance.save()
