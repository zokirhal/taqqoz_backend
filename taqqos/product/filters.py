import django_filters

from taqqos.product.models import Product, Category, Brand, Review


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all()
    )
    brand = django_filters.ModelMultipleChoiceFilter(
        queryset=Brand.objects.all()
    )

    class Meta:
        model = Product
        fields = (
            "category",
            "brand",
            "is_popular",
            "in_sale",
            "has_credit",
            "has_delivery",
        )


class ReviewFilter(django_filters.FilterSet):
    class Meta:
        model = Review
        fields = (
            "product",
        )
