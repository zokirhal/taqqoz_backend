from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from taqqos.account.models import User
from taqqos.account.serializers.user import UserSerializer


class UserView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(methods=["GET"], detail=False)
    def my_profile(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data)

    @action(methods=["PUT"], detail=False)
    def update_profile(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
