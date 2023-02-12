from django.db import models
from posts.models import Post

'''
property Model is a abstraction Model for
the Land and House Model it contains basic attributes that house and land has in common.
'''
class Property(models.Model): 

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



'''
Land Model 
inheritance: Property Model(Base Model)
'''

class Land(Property): 
    property_type = models.CharField(default="L",max_length=1)


'''
House Model
inheritance: Property Model(Base Model)
This model extra fields or attributes like numbers of rooms, number of floors, parking spaces etc. which is related to house
'''

'''
Requried Fields
no. of rooms : int
no. of floor : int 
parking spaces(area): float
facing side:(NORTH,EAST,WEST,SOUTH)
built date : Date
'''

class House(Property):
    property_type = models.CharField(default="H",max_length=1)
    no_of_bedrooms = models.IntegerField()
    no_of_bathrooms = models.IntegerField()
    no_of_floor = models.IntegerField()
    parking_area = models.PositiveIntegerField()
    facing_side = models.CharField(max_length=2)
    built_date = models.DateField()



    





    