from rest_framework.viewsets import ReadOnlyModelViewSet

from taqqos.product.filters import ProductFilter, ProductPriceFilter
from taqqos.product.models import Product, ProductPrice
from taqqos.product.serializers.product import ProductSerializer, ProductPriceSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ("name_uz", "name_ru")


class ProductPriceViewSet(ReadOnlyModelViewSet):
    queryset = ProductPrice.objects.all().order_by("-created_at")
    serializer_class = ProductPriceSerializer
    filterset_class = ProductPriceFilter
    search_fields = ("name",)
