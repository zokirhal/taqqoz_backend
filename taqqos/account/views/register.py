from django.conf import settings
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from taqqos.account.serializers.register import PhoneRegisterSerializer, PhoneRegisterVerifySerializer
from taqqos.account.services.register import phone_register, phone_register_verify


class RegisterView(GenericViewSet):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = []

    @action(methods=["POST"], detail=False, serializer_class=PhoneRegisterSerializer)
    def phone(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_register(**serializer.validated_data)
        res = serializer.data
        res["expire_duration"] = settings.SMS_CODE_EXPIRE
        return Response(res)

    @action(['POST'], detail=False, serializer_class=PhoneRegisterVerifySerializer)
    def phone_verify(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = phone_register_verify(serializer.user)
        return Response(res)
