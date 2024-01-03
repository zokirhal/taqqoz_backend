from django.conf import settings
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from taqqos.account.serializers.auth import PhoneSerializer, PhoneVerifySerializer, LogoutSerializer
from taqqos.account.services.auth import phone_auth, phone_verify


class PhoneAuthView(GenericViewSet):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == "logout":
            return (permissions.IsAuthenticated(), )
        return (permissions.AllowAny(), )

    def perform_authentication(self, request):
        if self.action == "logout":
            return super().get_authenticators()
        return []

    @action(methods=["POST"], detail=False, serializer_class=PhoneSerializer)
    def phone(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_auth(serializer.validated_data["phone_number"])
        res = serializer.data
        res["expire_duration"] = settings.SMS_CODE_EXPIRE
        return Response(res)

    @action(['POST'], detail=False, serializer_class=PhoneVerifySerializer)
    def phone_verify(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = phone_verify(serializer.user)
        return Response(res)

    @action(['POST'], detail=False, serializer_class=LogoutSerializer)
    def logout(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
