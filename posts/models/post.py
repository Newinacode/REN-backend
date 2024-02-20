
from django.db import models 
from django.conf import settings

class Post(models.Model):
    BUY = 'BY'
    SELL = 'SL'
    RENT = 'RT'


    PURPOSES =[
        (BUY,"buy"),
        (SELL,"sell"),
        (RENT,"rent")
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    purpose = models.CharField(max_length=2,choices=PURPOSES)
    street = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    longitude = models.DecimalField(max_digits=30, decimal_places=15)
    latitude = models.DecimalField(max_digits=30, decimal_places=15)
    def __str__(self) -> str:
        return f'{self.title}'

    class Meta:
        app_label = "posts"
