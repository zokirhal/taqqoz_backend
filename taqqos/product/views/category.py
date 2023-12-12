from rest_framework.viewsets import ReadOnlyModelViewSet

from taqqos.product.models import Category
from taqqos.product.serializers.category import CategorySerializer


class CategoryView(ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by("-order_number")
    serializer_class = CategorySerializer
    pagination_class = None
