from django.db import models
from django.conf import settings
class Post(models.Model):


    HOUSE = "H"
    LAND = "L"

    BUY = 'BY'
    SELL = 'SL'
    RENT = 'RT'

    TERAI = "TE"
    HILLY_OR_MOUNTAIN = "HM"

    PURPOSES =[
        (BUY,"buy"),
        (SELL,"sell"),
        (RENT,"rent")
    ]

    AREAS = [
        (TERAI,"terai"),
        (HILLY_OR_MOUNTAIN,"hilly and mountain")
    ]

    PROPERTY_TYPE = [
       ("H","house"),
        ("L","land")
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    purpose = models.CharField(max_length=2,choices=PURPOSES)
    area_formating = models.CharField(max_length=2,choices=AREAS)
    area1 = models.IntegerField()
    area2 = models.IntegerField()
    area3 = models.IntegerField()
    price = models.PositiveBigIntegerField()

    property_type = models.CharField(max_length=1,choices=PROPERTY_TYPE)

#house
    no_of_bedrooms = models.IntegerField()
    no_of_bathrooms = models.IntegerField()
    no_of_floor = models.IntegerField()
    parking_area = models.PositiveIntegerField()
    facing_side = models.CharField(max_length=2)
    built_date = models.DateField()


#map

    location = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    

    def __str__(self) -> str:
        return f'{self.title}'


# class Map(models.Model):
#     location = models.CharField(max_length=255)
#     street = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6)
#     post = models.OneToOneField(Post,on_delete=models.CASCADE,blank=True,null=True)
#     class Meta:
#         indexes = [
#             models.Index(fields=['location','city','street'], name='map_idx'),
#         ]

#     def __str__(self):
#         return f'{self.location} in {self.city}'
    