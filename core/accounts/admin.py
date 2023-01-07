from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "id",
        "email",
        "is_superuser",
        "is_active",
        "is_verified",
    )
    list_filter = ("email", "is_superuser", "is_active")
    search_fields = ("email",)
    ordering = ("-id",)
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "is_superuser", "is_verified")},
        ),
        (
            "Group Permissions",
            {
                "fields": ("groups", "user_permissions"),
            },
        ),
        (
            "Important Date",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
    )


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = [
        "id",
        "user",
        "first_name",
        "last_name",
        "phone_number",
        "is_complete",
        "is_author",
        "created_date",
    ]
    list_filter = ["is_complete", "is_author"]
    ordering = ("-id",)
    search_fields = ("first_name", "last_name")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, CustomUserAdmin)
