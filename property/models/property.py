from django.db import models
from posts.models.post import Post

'''
property Model is a abstraction Model for
the Land and House Model it contains basic attributes that house and land has in common.
'''
class Property(models.Model): 

    HOUSE = "H"
    LAND = "L"

    SELL = 'SL'
    RENT = 'RT'

    TERAI = "TE"
    HILLY_OR_MOUNTAIN = "HM"

    PURPOSES =[
        (SELL,"sell"),
        (RENT,"rent")
    ]

    AREAS = [
        (TERAI,"terai"),
        (HILLY_OR_MOUNTAIN,"hilly and mountain")
    ]

    PROPERTY_TYPE = [
       ("H","house"),
        ("L","land"),
        ('A',"Apartment"),
    ]

    post = models.OneToOneField(Post,on_delete=models.CASCADE,blank=True,null=True)
    purpose = models.CharField(max_length=2,choices=PURPOSES)
    area_formating = models.CharField(max_length=2,choices=AREAS)
    area1 = models.IntegerField()
    area2 = models.IntegerField()
    area3 = models.IntegerField()
    price = models.PositiveBigIntegerField()

    property_type = models.CharField(max_length=1,choices=PROPERTY_TYPE)


    class Meta: 
        abstract = True
        

