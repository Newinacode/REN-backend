from django.contrib import admin

from .models.OTP import OTP
from .models.user import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "name",
        "mobile_number",
        "is_verified",
        "is_admin",
        "is_active",
    )
    list_filter = ("is_admin", "is_verified", "is_active")
    search_fields = ("email", "name", "mobile_number")
    ordering = ("-id",)

    def save_model(self, request, obj, form, change):
        """Hash passwords entered through the admin add/change form."""
        password = form.cleaned_data.get("password")
        if password and not password.startswith(
            ("pbkdf2_", "argon2$", "scrypt$", "bcrypt$")
        ):
            obj.set_password(password)
        super().save_model(request, obj, form, change)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "otp_number")
    search_fields = ("user__email",)
