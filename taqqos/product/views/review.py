from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from taqqos.product.filters import ReviewFilter
from taqqos.product.models import Review
from taqqos.product.serializers.review import ReviewSerializer


class ReviewViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filterset_class = ReviewFilter

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return (permissions.AllowAny(), )
        return (permissions.IsAuthenticated(), )

    def perform_authentication(self, request):
        if self.action in ["list", "retrieve"]:
            return []
        return super().get_authenticators()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


__all__ = [
    "ReviewViewSet"
]
