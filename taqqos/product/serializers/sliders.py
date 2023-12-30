from django.utils.translation import get_language
from rest_framework import serializers

from taqqos.document.serializers import FileSerializer
from taqqos.product.models import Slider, Seller


class SliderSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    image = FileSerializer()

    class Meta:
        model = Slider
        fields = (
            "id",
            "name",
            "text",
            "image"
        )

    def get_name(self, instance: Slider) -> str:
        return getattr(instance, f"name_{get_language()}")

    def get_text(self, instance: Slider) -> str:
        return getattr(instance, f"text_{get_language()}")


class SellerSerializer(serializers.ModelSerializer):
    image = FileSerializer()

    class Meta:
        model = Seller
        fields = (
            "id",
            "image"
        )
