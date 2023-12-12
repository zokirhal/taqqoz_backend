from django.urls import path, include


# Project
from taqqos.geo.views import RegionListView

urlpatterns = [
    path('region', RegionListView.as_view())
]
