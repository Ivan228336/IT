from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from modules.core.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {"fields": ("username", "photo", "status")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("date_joined",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "id",
        "username",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_display_links = ("id", "username")
    list_editable = ("is_active",)
    search_fields = ("email",)

    readonly_fields = ("date_joined",)
