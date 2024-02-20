from django.contrib import admin

# Register your models here.


from .models.saved_house import SavedHome


admin.site.register(SavedHome)