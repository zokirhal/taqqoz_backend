from typing import List

from django.utils.translation import get_language
from rest_framework import serializers

from taqqos.document.serializers import FileSerializer
from taqqos.product.models import Category
from taqqos.product.serializers.attribute import AttributeSerializer
from taqqos.product.serializers.brand import BrandSerializer


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField(
        read_only=True, method_name="get_child_categories"
    )
    icon = FileSerializer()
    brands = BrandSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "icon",
            "brands",
            "children"
        )

    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)
        action = self.context["view"].action
        if action == "retrieve":
            self.fields["attributes"] = AttributeSerializer(many=True)

    def get_name(self, instance: Category) -> str:
        return getattr(instance, f"name_{get_language()}")

    def get_child_categories(self, instance: Category) -> List[Category]:
        if instance.children:
            serializer = CategorySerializer(
                instance=instance.children.all().order_by("order_number"),
                many=True,
                context=self.context,
            )
            return serializer.data
        else:
            return None
