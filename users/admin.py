from django.contrib import admin

# Register your models here.


from .models import Recommendation,SavedHome

admin.site.register(Recommendation)
admin.site.register(SavedHome)