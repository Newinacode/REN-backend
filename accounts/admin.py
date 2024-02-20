from django.contrib import admin
from .models.user import CustomUser
from .models.OTP import OTP


admin.site.register(CustomUser)
admin.site.register(OTP)