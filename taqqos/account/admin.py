from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from taqqos.account.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id", "phone_number", "full_name", "is_staff", "is_active", "is_superuser", "date_joined",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "username",
                    "full_name",
                    "password",
                )
            },
        ),
        (
            _("Личная информация"),
            {
                "fields": (
                    "profile_image",
                    "sms_date",
                    "sms_code",
                    "is_demo",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "full_name",
                    "password1",
                    "password2",
                )
            },
        ),
    )
    search_fields = ("phone_number", "full_name")
    ordering = ("-date_joined",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
