from django.contrib import admin

# Register your models here.

from .models import House,Land
admin.site.register(House)
admin.site.register(Land)