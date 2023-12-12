from datetime import timedelta

from django.conf import settings
from django.utils.translation import gettext as _
from django.utils import timezone

from rest_framework import serializers

from taqqos.account.models import User
from taqqos.core.serializers import CustomPhoneNumberField


class PhoneRegisterSerializer(serializers.Serializer):
    phone_number = CustomPhoneNumberField(required=True)

    def validate_phone_number(self, phone_number):
        if User.objects.filter(phone_number=phone_number, is_active=True).exists():
            raise serializers.ValidationError(_("User found with this phone number"))
        return phone_number


class PhoneRegisterVerifySerializer(serializers.Serializer):
    phone_number = CustomPhoneNumberField(required=True)
    sms_code = serializers.IntegerField(required=True, max_value=9999, min_value=1000)

    def validate(self, attrs):
        now = timezone.now()
        phone_number = attrs['phone_number']
        sms_code = attrs['sms_code']
        user = self.user = User.objects.filter(
            phone_number=phone_number,
            sms_code=sms_code,
            is_active=False
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
