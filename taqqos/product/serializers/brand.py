from django.utils.translation import get_language
from rest_framework import serializers

from taqqos.product.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField(
        read_only=True, method_name="get_child_categories"
    )

    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
            "children",
        )

    def get_name(self, instance):
        return getattr(instance, f"name_{get_language()}")

    def get_child_categories(self, obj):
        if obj.children:
            serializer = BrandSerializer(
                instance=obj.children.all().order_by("order_number"),
                many=True,
                context=self.context,
            )
            return serializer.data
        else:
            return None
