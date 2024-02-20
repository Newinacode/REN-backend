from django.contrib import admin

# Register your models here.

from .models.land import Land
from .models.house import House

admin.site.register(House)
admin.site.register(Land)