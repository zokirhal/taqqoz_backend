from django.utils.translation import get_language
from rest_framework import serializers

from taqqos.document.serializers import FileSerializer
from taqqos.product.models import Slider, Seller


class SliderSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="image.file")
    image_mobile = serializers.ImageField(source="image_mobile.file")

    class Meta:
        model = Slider
        fields = (
            "id",
            "image",
            "image_mobile"
        )


class SellerSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="image.file")

    class Meta:
        model = Seller
        fields = (
            "id",
            "image"
        )
