# python
import logging

# django
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import PermissionDenied

# project
#from udb.core.tasks import send_sms_with_play_mobile


class UserManager(BaseUserManager):
    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone_number must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        phone_number = extra_fields.pop("phone_number")
        password = extra_fields.pop("password")
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)

    def verify_phone(self, data):
        phone_number = data["phone_number"]
        unique_key = data["unique_key"]
        user, created = self.get_or_create(phone_number=phone_number)
        if created:
            user.is_active = False
        user.save()
        if user.is_demo:
            code = user.demo_verification_code
        else:
            code = f"{self.model.generate_code()}"
            text = (
                f"Код подключения: {code} "
                f"Никому не сообщайте его {unique_key}",
            )
            #send_sms_with_play_mobile.delay(phone_number, text)
        key = self.model.set_cache(code, user, ttl=settings.CACHE_TTL)
        logging.warning(code)
        data = {
            "type": "SMS_CODE_REQUIRED",
            "info": {
                "sms_code_key": key,
                "available_duration": settings.CACHE_TTL,
                "send_code_timeout": 60,
            },
        }
        # send_sms.delay(phone_number, sms_code)
        return data

    def verify_registration(self, user):
        key = self.model.set_register_cache(user)
        data = {
            "type": "REGISTRATION_REQUIRED",
            "info": {"registration_key": key, "available_duration": 600},
        }
        return data

    def validate_user_status(self, phone_number):
        user = self.filter(phone_number=phone_number)
        if (
            user.exists()
            and user.first().user_status == self.model.UserStatus.BLOCKED
        ):
            raise PermissionDenied("You have been blocked!")
