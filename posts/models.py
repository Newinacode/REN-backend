from django.db import models
from django.conf import settings
class Post(models.Model):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self) -> str:
        return f'{self.title}'


class Map(models.Model):
    location = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    post = models.OneToOneField(Post,on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        indexes = [
            models.Index(fields=['location','city','street'], name='map_idx'),
        ]

    def __str__(self):
        return f'{self.location} in {self.city}'
    