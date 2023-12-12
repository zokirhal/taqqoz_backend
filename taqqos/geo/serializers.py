from rest_framework import serializers

from taqqos.geo.models import Region, District


class DistrictListSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = (
            "id",
            "name",
        )


class RegionListSerializer(serializers.ModelSerializer):
    districts = DistrictListSerializer(many=True)

    class Meta:
        model = Region
        fields = (
            "id",
            "name",
            "districts",
        )


class DistrictSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = (
            "id",
            "name",
            "region",
        )

    def get_region(self, instance):
        return {
            "id": instance.region.id,
            "name": instance.region.name
        }
