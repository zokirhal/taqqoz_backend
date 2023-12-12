from rest_framework.generics import ListAPIView

from taqqos.geo.models import Region
from taqqos.geo.serializers import RegionListSerializer


class RegionListView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionListSerializer
    pagination_class = None
    permission_classes = []
    authentication_classes = []
