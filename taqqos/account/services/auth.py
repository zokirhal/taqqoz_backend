from django.utils.translation import gettext as _
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from taqqos.account.models import User
from taqqos.account.serializers.user import UserSerializer
from taqqos.core.utils import send_sms_verification


def phone_auth(phone_number: str) -> bool:
    try:
        user, created = User.objects.get_or_create(
            phone_number=phone_number,
            defaults=dict(
                is_active=False,
            ))
        send_sms_verification(
            user,
            phone_number,
            _('Taqqoz dlya vhoda SMS-kod: %s')
        )
    except Exception as e:
        raise ValidationError({
            'non_field_errors': [e]
        })


def phone_verify(user: User) -> dict:
    refresh = RefreshToken.for_user(user)
    if not user.is_demo:
        user.sms_code = ""
    user.last_login = timezone.now()
    if user.full_name:
        user_data = UserSerializer(instance=user).data
    else:
        user_data = {}
    user.is_active = True
    user.save()
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user_data': user_data
    }
