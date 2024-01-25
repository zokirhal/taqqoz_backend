from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from taqqos.product.filters import ProductFilter, ProductPriceFilter
from taqqos.product.models import Product, ProductPrice, ProductAttribute, Option, Attribute
from taqqos.product.serializers.product import ProductSerializer, ProductPriceSerializer, ProductPriceCreateSerializer
from taqqos.product.services import create_product_price


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ("name_uz", "name_ru")

    def get_queryset(self):
        query_params = dict(self.request.query_params)
        excluding_fields = self.filterset_class.Meta.fields + ("page", "page_size")
        for field in excluding_fields:
            query_params.pop(field, "")
        product_attributes = []
        for key, val in query_params.items():
            key = key.split("_")
            if len(key) != 2:
                continue
            option = Option.objects.filter(Q(attribute__code=key[0]) & Q(code=key[1])).first()
            p_atts = []
            if option:
                if option.attribute.type == Attribute.TEXT:
                    if option.code == "from":
                        p_atts = ProductAttribute.objects.filter(attribute=option.attribute, option__vaue__gte=val)
                    if option.code == "to":
                        p_atts = ProductAttribute.objects.filter(attribute=option.attribute, option__vaue__lte=val)
                else:
                    p_atts = ProductAttribute.objects.filter(option=option)
                product_attributes.extend(p_atts)
        qs = self.filter_queryset(self.queryset)
        if query_params:
            qs = qs.filter(attributes__in=product_attributes).distinct()
        return qs


class ProductPriceViewSet(ReadOnlyModelViewSet):
    queryset = ProductPrice.objects.all().order_by("-created_at")
    serializer_class = ProductPriceSerializer
    filterset_class = ProductPriceFilter
    search_fields = ("name",)


class ProductPriceCreateView(APIView):
    @swagger_auto_schema(request_body=ProductPriceCreateSerializer())
    def post(self, request, *args, **kwargs):
        serializer = ProductPriceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        create_product_price.delay(data)
        return Response(serializer.data)
