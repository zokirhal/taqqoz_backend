from django.urls import include, path
from rest_framework import routers

from taqqos.document.views import FileViewSet

router = routers.DefaultRouter()
router.register(r"file", FileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
