from django.utils.translation import get_language
from rest_framework import serializers

from taqqos.document.serializers import FileSerializer
from taqqos.product.models import Product, ProductImage, ProductAttribute, ProductFeature, ProductVideoReview, \
    ProductPrice
from taqqos.product.serializers.attribute import OptionSerializer, AttributeMiniSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    photo = FileSerializer()

    class Meta:
        model = ProductImage
        fields = (
            "id",
            "photo"
        )


class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeMiniSerializer()
    option = OptionSerializer()

    class Meta:
        model = ProductAttribute
        fields = (
            "id",
            "attribute",
            "option"
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
    photo = FileSerializer()

    class Meta:
        model = ProductPrice
        fields = (
            "id",
            "name",
            "price_amount",
            "photo",
            "description",
            "features",
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
            "slug",
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
            self.fields["attributes"] = ProductAttributeSerializer(many=True)
            self.fields["video_reviews"] = ProductVideoReviewSerializer(many=True)
            self.fields["product_prices"] = ProductPriceSerializer(many=True)

    def get_name(self, instance: Product) -> str:
        return getattr(instance, f"name_{get_language()}")

    def get_description(self, instance: Product) -> str:
        return getattr(instance, f"description_{get_language()}")


class ProductDetailSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    photo = FileSerializer()
    images = ProductImageSerializer(many=True)
    attributes = ProductAttributeSerializer(many=True)
    video_reviews = ProductVideoReviewSerializer(many=True)
    product_prices = ProductPriceSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
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
            "description",
            "images",
            "attributes",
            "video_reviews",
            "product_prices",
        )

    def get_name(self, instance: Product) -> str:
        return getattr(instance, f"name_{get_language()}")

    def get_description(self, instance: Product) -> str:
        return getattr(instance, f"description_{get_language()}")

class ProductPriceCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=512)
    price_amount = serializers.DecimalField(max_digits=18, decimal_places=2,)
    photo = serializers.CharField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)
    features = serializers.JSONField(required=False, allow_null=True)
    has_credit = serializers.BooleanField(default=False, required=False, allow_null=True)
    credit_monthly_amount = serializers.CharField(required=False, allow_null=True)
    has_delivery = serializers.BooleanField(default=False, required=False, allow_null=True)
    delivery_info = serializers.CharField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True)
    website = serializers.CharField(required=True)
    website_link = serializers.CharField(required=True)
