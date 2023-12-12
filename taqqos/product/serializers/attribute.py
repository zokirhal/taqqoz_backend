from django.utils.translation import get_language
from rest_framework import serializers

from taqqos.product.models import Attribute, Option


class OptionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = (
            "id",
            "name",
            "code",
            "label"
        )

    def get_name(self, instance):
        return getattr(instance, f"name_{get_language()}")


class AttributeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    options = OptionSerializer(many=True)

    class Meta:
        model = Attribute
        fields = (
            "id",
            "name",
            "code",
            "type",
            "is_required",
            "can_join",
            "options"
        )

    def get_name(self, instance):
        return getattr(instance, f"name_{get_language()}")