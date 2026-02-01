from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Bus, Line, Trip, Driver

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_staff", "is_driver", "is_citizen")
    list_filter = ("is_staff", "is_driver", "is_citizen")
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_driver", "is_citizen")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_driver", "is_citizen"),
        }),
    )

admin.site.register(Bus)
admin.site.register(Line)
admin.site.register(Trip)
admin.site.register(Driver)
