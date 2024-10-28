from typing import Any

from django_select2 import forms as s2forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin, TabularInline, StackedInline

from .forms import ProductAttributeForm
from taqqos.product.models import (
    Attribute,
    Category,
    Product,
    Option,
    Brand,
    ProductAttribute,
    ProductPrice,
    ProductFeature,
    ProductVideoReview,
    ProductImage,
    Review,
    ReviewFile,
    Favourite,
    Slider,
    Seller,
)


class PhotoWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = (
        "id",
        "name_uz",
    )
    search_fields = ["name_uz", "name_ru"]
    list_display_links = ["id", "name_uz"]


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = (
        "id",
        "name_uz",
    )
    exclude = ("icon",)
    search_fields = ["name_uz", "name_ru"]
    list_display_links = ["id", "name_uz"]


class ProductFeatureAdmin(StackedInline):
    model = ProductFeature
    list_display = (
        "id",
        "name_uz",
    )
    extra = 1


class ProductVideoReviewAdmin(StackedInline):
    model = ProductVideoReview
    list_display = (
        "id",
        "link",
    )
    extra = 1


class ProductImageeAdmin(TabularInline):
    model = ProductImage
    list_display = (
        "id",
        "photo",
    )
    extra = 1


class ProductAttributeAdmin(TabularInline):
    model = ProductAttribute
    form = ProductAttributeForm
    list_display = (
        "id",
        "attribute",
        "option",
    )
    extra = 1


class ProductPriceInlineAdmin(TabularInline):
    model = Product.product_prices.through
    list_display = ("id", "name")
    extra = 0
    autocomplete_fields = ["productprice"]

    def has_change_permission(self, *args, **kwargs):
        return False

    def get_queryset(self, request):
        qs = super(ProductPriceInlineAdmin, self).get_queryset(request)
        return qs.prefetch_related("product")


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    autocomplete_fields = ["category", "brand", "product_prices"]
    list_display = (
        "id",
        "name_uz",
        "category",
        "brand",
        "is_popular",
        # "file_tag"
    )
    list_display_links = ["id", "name_uz"]
    list_filter = ["brand", "category", "is_popular", "created_at"]
    prepopulated_fields = {"slug": ("name_uz",)}
    ordering = ("-updated_at",)
    search_fields = ["name_uz", "name_ru", "description_uz", "description_ru"]
    date_hierarchy = "created_at"
    inlines = [
        ProductImageeAdmin,
        ProductAttributeAdmin,
        ProductVideoReviewAdmin,
        ProductPriceInlineAdmin,
        # ProductFeatureAdmin,
    ]

    def file_tag(self, obj: Product) -> Any:
        if obj.photo:
            return mark_safe(
                '<img src="{}" height="50" weight="50"/>'.format(obj.photo.url)
            )
        return None

    file_tag.short_description = "краткий изображение"

    def save_model(self, request, obj, form, change):
        if change:
            print("updating a product")
            super().save_model(request, obj, form, change)
        else:
            print("creating a product")
            super().save_model(request, obj, form, change)

            product = obj
            matched_product_prices = []
            for product_price in ProductPrice.objects.all():
                product_name_words = product.short_name.lower().split(" ")
                every_word_in_name = True
                for word in product_name_words:
                    if word not in product_price.name.lower():
                        every_word_in_name = False
                if every_word_in_name:
                    matched_product_prices.append(product_price)

            if matched_product_prices:
                product.product_prices.add(*matched_product_prices)
                product.save()


class OptionAdmin(StackedInline):
    model = Option
    list_display = (
        "id",
        "name_uzbek",
    )
    extra = 1


@admin.register(Attribute)
class AttributeAdmin(ModelAdmin):
    list_display = (
        "id",
        "name_uz",
        "code",
        "type",
        "is_required",
    )
    list_display_links = ["id"]
    list_filter = [
        "type",
        "categories",
        "is_required",
    ]
    search_fields = ["name_uz", "name_ru"]
    inlines = [
        OptionAdmin,
    ]


@admin.register(ProductPrice)
class ProductPriceAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "price_amount",
        "has_credit",
        "has_delivery",
        "address",
        "phone_number",
        "website",
        # "file_tag",
    )
    exclude = ("photo",)

    list_display_links = ["id", "name"]
    list_filter = ["has_credit", "has_delivery", "website"]
    search_fields = ["name"]

    # def file_tag(self, obj: ProductPrice) -> Any:
    #     if obj.photo:
    #         return mark_safe(
    #             '<img src="{}" height="50"/>'.format(obj.photo.thumbnail.url)
    #         )

    #     elif obj.image_url:
    #         return mark_safe('<img src="{}" height="50"/>'.format(obj.image_url))

    #     return None

    # file_tag.short_description = "краткий изображение"


class ReviewFileAdmin(admin.StackedInline):
    model = ReviewFile
    list_display = (
        "id",
        "file",
    )
    extra = 0


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("id", "user", "product", "rate", "text", "created_at")
    list_filter = ["rate"]
    search_fields = ["text"]
    inlines = [ReviewFileAdmin]


@admin.register(Favourite)
class FavouriteAdmin(ModelAdmin):
    list_display = ("id", "user", "product", "created_at")


@admin.register(Slider)
class SliderAdmin(ModelAdmin):
    list_display = (
        "id",
        "image",
    )


@admin.register(Seller)
class SellerAdmin(ModelAdmin):
    list_display = (
        "id",
        "image",
    )
