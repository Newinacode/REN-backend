from django.db import models
from accounts.models.user import CustomUser
from posts.models.post import Post


class Profile(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()