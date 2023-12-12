import re

from django.db import transaction
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import MultiPartParser

# Project
from taqqos.document.models import File, FILE_TYPES
from taqqos.document.serializers import FileSerializer
from taqqos.document.services import create_video_preview, create_thumbnail_image


class FileViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  GenericViewSet):
    queryset = File.objects.all()
    permission_classes = (AllowAny,)
    authentication_classes = []
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            instance = serializer.save()
            thumb_extension = str(instance.file.name).split(".")[-1]
            file_type = None
            for key, val in FILE_TYPES.items():
                if re.match(key, thumb_extension):
                    file_type = val
                    break
            instance.file_type = file_type
            instance.save()
            match file_type:
                case File.VIDEO:
                    create_video_preview(instance)
                case File.IMAGE:
                    create_thumbnail_image(instance)
        return Response(serializer.data)
