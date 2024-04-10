from typing import Any

from django import forms
from django_select2 import forms as s2forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django_select2.forms import Select2Widget
from mptt.admin import DraggableMPTTAdmin

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
    Favourite, Slider, Seller,
)


class PhotoWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]


class ProductFeatureAdmin(admin.StackedInline):
    model = ProductFeature
    list_display = (
        "id",
        "name_uz",
    )
    extra = 1


class ProductVideoReviewAdmin(admin.StackedInline):
    model = ProductVideoReview
    list_display = (
        "id",
        "link",
    )
    extra = 1


class ProductProductImageInlineForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = (
            "id",
            'photo',
        )
        widgets = {
            'photo': Select2Widget
        }


class ProductImageeAdmin(admin.StackedInline):
    model = ProductImage
    form = ProductProductImageInlineForm
    list_display = (
        "id",
        "photo",
    )
    extra = 1


class ProductAttributeAdmin(admin.StackedInline):
    model = ProductAttribute
    list_display = (
        "id",
        "attribute",
    )
    extra = 1


class ProductPriceInlineAdmin(admin.TabularInline):
    model = ProductPrice.products.through
    list_display = (
        "id",
        "name"
    )
    extra = 1


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            'photo': Select2Widget
        }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = (
        "id",
        "name_uz",
        "category",
        "brand",
        "is_popular",
        "file_tag"
    )
    list_display_links = ["id"]
    list_filter = [
        "brand",
        "category",
        "is_popular",
        "created_at"
    ]
    prepopulated_fields = {"slug": ("name_uz", )}
    ordering = ("-updated_at",)
    search_fields = ["name_uz", "name_ru", "description_uz", "description_ru"]
    date_hierarchy = "created_at"
    inlines = [
        ProductImageeAdmin,
        ProductAttributeAdmin,
        ProductVideoReviewAdmin,
        ProductPriceInlineAdmin
        # ProductFeatureAdmin,
    ]

    def file_tag(self, obj: Product) -> Any:
        if obj.photo:
            return mark_safe(
                '<img src="{}" height="50"/>'.format(obj.photo.thumbnail.url)
            )
        return None

    file_tag.short_description = "краткий изображение"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        product = obj
        product.product_prices.clear()
        product_prices = ProductPrice.objects.filter(
            name__icontains=product.short_name
        )
        if product_prices:
            print(product.short_name)
            print(product_prices.values_list("name"))
            product.product_prices.add(*product_prices)
        product.save()


class OptionAdmin(admin.StackedInline):
    model = Option
    list_display = (
        "id",
        "name_uz",
    )
    extra = 1


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name_uz",
        "code",
        "type",
        "is_required",
    )
    list_display_links = ["id"]
    list_filter = ["type", "categories", "is_required", ]
    search_fields = ["name_uz", "name_ru"]
    inlines = [
        OptionAdmin,
    ]


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price_amount",
        "has_credit",
        "has_delivery",
        "address",
        "phone_number",
        "website",
        "file_tag"
    )
    list_display_links = ["id"]
    list_filter = ["has_credit", "has_delivery", "website"]
    search_fields = ["name"]

    def file_tag(self, obj: Product) -> Any:
        if obj.photo:
            return mark_safe(
                '<img src="{}" height="50"/>'.format(obj.photo.thumbnail.url)
            )
        return None

    file_tag.short_description = "краткий изображение"


admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        "tree_actions",
        "indented_title",
        # ...more fields if you feel like it...
    ),
    list_display_links=("indented_title",),
)


admin.site.register(
    Brand,
    DraggableMPTTAdmin,
    list_display=(
        "tree_actions",
        "indented_title",
        # ...more fields if you feel like it...
    ),
    list_display_links=("indented_title",),
)


class ReviewFileAdmin(admin.StackedInline):
    model = ReviewFile
    list_display = (
        "id",
        "file",
    )
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "rate",
        "text",
        "created_at"
    )
    list_filter = ["rate"]
    search_fields = ["text"]
    inlines = [ReviewFileAdmin]


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "created_at"
    )


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image",
    )


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image",
    )