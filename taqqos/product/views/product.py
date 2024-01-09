from django.db.models import Q
from rest_framework.viewsets import ReadOnlyModelViewSet

from taqqos.product.filters import ProductFilter, ProductPriceFilter
from taqqos.product.models import Product, ProductPrice, ProductAttribute, Option, Attribute
from taqqos.product.serializers.product import ProductSerializer, ProductPriceSerializer


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
        if product_attributes:
            qs = qs.filter(attributes__in=product_attributes).distinct()
        return qs


class ProductPriceViewSet(ReadOnlyModelViewSet):
    queryset = ProductPrice.objects.all().order_by("-created_at")
    serializer_class = ProductPriceSerializer
    filterset_class = ProductPriceFilter
    search_fields = ("name",)
