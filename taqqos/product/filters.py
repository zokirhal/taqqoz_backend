import django_filters
from django.db.models import Q, Count

from taqqos.product.models import Product, Category, Brand, Review, ProductPrice


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all()
    )
    brand = django_filters.ModelMultipleChoiceFilter(
        queryset=Brand.objects.all()
    )
    min_price = django_filters.NumberFilter(method="get_min_price_filter")
    max_price = django_filters.NumberFilter(method="get_max_price_filter")

    has_credit = django_filters.BooleanFilter(method="get_has_credit_filter")
    has_delivery = django_filters.BooleanFilter(method="get_has_delivery_filter")
    is_popular = django_filters.BooleanFilter(method="get_has_is_popular_filter")

    class Meta:
        model = Product
        fields = (
            "category",
            "brand",
            "is_popular",
            "min_price",
            "max_price",
            "has_credit",
            "has_delivery"
        )

    def get_min_price_filter(self, queryset, name, value, *args, **kwargs):
        product_prices = ProductPrice.objects.filter(price_amount__gte=value)
        return queryset.filter(product_prices__in=product_prices)

    def get_max_price_filter(self, queryset, name, value, *args, **kwargs):
        product_prices = ProductPrice.objects.filter(price_amount__lte=value)
        return queryset.filter(product_prices__in=product_prices)

    def get_has_credit_filter(self, queryset, name, value, *args, **kwargs):
        product_prices = ProductPrice.objects.filter(has_credit=value)
        return queryset.filter(product_prices__in=product_prices)

    def get_has_delivery_filter(self, queryset, name, value, *args, **kwargs):
        product_prices = ProductPrice.objects.filter(has_delivery=value)
        return queryset.filter(product_prices__in=product_prices)

    def get_has_is_popular_filter(self, queryset, name, value, *args, **kwargs):
        queryset = queryset.annotate(
            rate_counts=Count("reviews"),
            favorite_counts=Count("favorites")
        ).order_by("-rate_counts", "-views", "-favorite_counts")
        return queryset


class ProductPriceFilter(django_filters.FilterSet):
    class Meta:
        model = ProductPrice
        fields = (
            "products",
        )


class ReviewFilter(django_filters.FilterSet):
    class Meta:
        model = Review
        fields = (
            "product",
        )
