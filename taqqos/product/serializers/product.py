from django.utils.translation import get_language
from rest_framework import serializers

from taqqos.document.serializers import FileSerializer
from taqqos.product.models import Product, ProductImage, ProductAttribute, ProductFeature, ProductVideoReview, \
    ProductPrice


class ProductImageSerializer(serializers.ModelSerializer):
    photo = FileSerializer()

    class Meta:
        model = ProductImage
        fields = (
            "id",
            "photo"
        )


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = (
            "id",
            "attribute",
            "text_value",
            "toggle_value",
            "options"
        )


class ProductFeatureSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = ProductFeature
        fields = (
            "id",
            "name",
            "value",
        )

    def get_name(self, instance: ProductFeature) -> str:
        return getattr(instance, f"name_{get_language()}")


class ProductVideoReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideoReview
        fields = (
            "id",
            "link",
        )


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = (
            "id",
            "name",
            "price_amount",
            "description",
            "feature",
            "has_credit",
            "credit_monthly_amount",
            "has_delivery",
            "delivery_info",
            "address",
            "phone_number",
            "website",
            "website_link"
        )


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    photo = FileSerializer()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "brand",
            "photo",
            "is_popular",
            "views",
            "rate",
            "review_count",
            "min_price",
            "price_count",
            "has_credit",
            "has_delivery",
            "description"
        )

    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        action = self.context["view"].action
        if action == "retrieve":
            self.fields["images"] = ProductImageSerializer(many=True)
            self.fields["features"] = ProductFeatureSerializer(many=True)
            self.fields["video_reviews"] = ProductVideoReviewSerializer(many=True)
            self.fields["product_prices"] = ProductPriceSerializer(many=True)

    def get_name(self, instance: Product) -> str:
        return getattr(instance, f"name_{get_language()}")

    def get_description(self, instance: Product) -> str:
        return getattr(instance, f"description_{get_language()}")
