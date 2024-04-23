from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Register your models here.
User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin, admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('username', 'first_name', 'second_name', 'last_name')
    search_fields = ('username', 'first_name', 'second_name', 'last_name')
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
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
                "classes": ("wide",),
                "fields": ("username", "first_name", "last_name", "second_name", "password1", "password2"),
            },
        ),
    )