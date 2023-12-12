# django
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

# installed package
from phonenumber_field.modelfields import PhoneNumberField

# project import
from taqqos.account.managers import UserManager
from taqqos.document.models import File


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(_("номер телефона"), unique=True, db_index=True)
    full_name = models.CharField(_("полное имя"), max_length=150, blank=True, db_index=True, null=True)
    username = models.CharField(_("имя пользователя"), max_length=255, db_index=True, null=True, blank=True)
    profile_image = models.ForeignKey(
        File, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="изображение профиля",
    )
    is_staff = models.BooleanField(
        _("статус персонала"),
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        _("активный"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("дата присоединения"), default=timezone.now)

    sms_date = models.DateTimeField(_("смс свидание"), null=True, blank=True)
    sms_code = models.CharField(_("смс-код"), max_length=128, blank=True, null=True)
    is_demo = models.BooleanField(_("это демо"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    class Meta:
        verbose_name = _("пользователь")
        verbose_name_plural = _("пользователи")

    def __str__(self):
        return f"{self.phone_number}"

