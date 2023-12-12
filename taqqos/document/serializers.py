from rest_framework import serializers

from taqqos.document.models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'file_type', 'thumbnail')
        read_only_fields = ('thumbnail', 'file_type')

