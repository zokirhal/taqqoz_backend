from rest_framework.generics import ListAPIView

from taqqos.product.models import Slider, Seller
from taqqos.product.serializers.sliders import SliderSerializer, SellerSerializer


class SliderView(ListAPIView):
    queryset = Slider.objects.all().order_by("order_number")
    serializer_class = SliderSerializer
    pagination_class = None


class SellerView(ListAPIView):
    queryset = Seller.objects.all().order_by("order_number")
    serializer_class = SellerSerializer
    pagination_class = None
