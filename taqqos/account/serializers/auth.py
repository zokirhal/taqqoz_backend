from datetime import timedelta

from django.conf import settings
from django.utils.translation import gettext as _
from django.utils import timezone
from rest_framework import serializers

from taqqos.account.models import User
from taqqos.core.serializers import CustomPhoneNumberField


class PhoneSerializer(serializers.Serializer):
    phone_number = CustomPhoneNumberField(required=True)


class PhoneVerifySerializer(serializers.Serializer):
    phone_number = CustomPhoneNumberField(required=True)
    sms_code = serializers.IntegerField(required=True, max_value=9999, min_value=1000)

    def validate(self, attrs):
        now = timezone.now()
        phone_number = attrs['phone_number']
        sms_code = attrs['sms_code']
        user = self.user = User.objects.filter(
            phone_number=phone_number,
            sms_code=sms_code,
        ).first()

        if not user:
            raise serializers.ValidationError({
                'non_field_errors': [_('Wrong sms code.')]
            })

        if now > (user.sms_date + timedelta(seconds=settings.SMS_CODE_EXPIRE)):
            raise serializers.ValidationError({
                'non_field_errors': [_('Sms code is expired.')]
            })
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
