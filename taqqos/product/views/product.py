from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from taqqos.product.filters import ProductFilter, ProductPriceFilter, CustomOrderFilter
from taqqos.product.models import Product, ProductPrice, ProductAttribute, Attribute
from taqqos.product.serializers.product import ProductSerializer, ProductPriceSerializer, ProductPriceCreateSerializer
from taqqos.product.services import create_product_price


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        CustomOrderFilter
    ]
    filterset_class = ProductFilter
    search_fields = ("name_uz", "name_ru")
    ordering_fields = ("price", "is_popular", "views", "id", "created_at")
    ordering_case_insensitive_fields = ("price", "is_popular")


def get_queryset(self):
        qs = self.filter_queryset(self.queryset)
        query_params = dict(self.request.query_params)
        excluding_fields = self.filterset_class.Meta.fields + ("page", "page_size", "ordering")
        for field in excluding_fields:
            query_params.pop(field, "")
        product_attributes = []
        for key, val in query_params.items():
            val = val[0]
            attribute = Attribute.objects.filter(code=key).first()
            if not attribute:
                continue
            if attribute.type == Attribute.TEXT:
                min_val, max_val = val.split(",")
                p_atts = ProductAttribute.objects.filter(
                    attribute=attribute
                )
                if max_val and min_val:
                    p_atts = p_atts.filter(
                        Q(option__value__gte=min_val) & Q(option__value__lte=max_val)
                    )
                if min_val:
                    p_atts = p_atts.filter(option__value__gte=min_val)
                if max_val:
                    p_atts = p_atts.filter(option__value__lte=max_val)
            else:
                values = val.split(",") if "," in val else [val]
                p_atts = ProductAttribute.objects.filter(attribute=attribute, option__value__in=values)
            if p_atts:
                product_attributes.extend(p_atts)
        if product_attributes:
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
