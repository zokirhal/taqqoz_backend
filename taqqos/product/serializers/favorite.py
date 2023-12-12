from django.utils.translation import gettext as _

from rest_framework import serializers

from taqqos.product.models import Favourite
from taqqos.product.serializers.product import ProductSerializer


class FavouriteSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        self.fields["product"] = ProductSerializer(context=self.context)
        return super().to_representation(instance)

    class Meta:
        model = Favourite
        fields = (
            "id",
            "product",
        )

    def validate(self, attrs):
        product = attrs["product"]
        user = self.context["request"].user
        if Favourite.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError({
                "detail": _("This business has already added to your favourite list")
            })
        return attrs
