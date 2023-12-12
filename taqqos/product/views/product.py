from rest_framework.viewsets import ReadOnlyModelViewSet

from taqqos.product.filters import ProductFilter
from taqqos.product.models import Product
from taqqos.product.serializers.product import ProductSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
