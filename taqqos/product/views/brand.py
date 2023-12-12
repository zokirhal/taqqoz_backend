from rest_framework.generics import ListAPIView

from taqqos.product.models import Brand
from taqqos.product.serializers.brand import BrandSerializer


class BrandView(ListAPIView):
    queryset = Brand.objects.all().order_by("-order_number")
    serializer_class = BrandSerializer
    pagination_class = None
