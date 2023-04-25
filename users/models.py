from django.db import models
from accounts.models import CustomUser
# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    

class Location(models.Model): 
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    longitude = models.DecimalField()
    longitude = models.DecimalField()




