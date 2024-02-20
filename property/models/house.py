
from django.db import models
from .property import Property

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

    class Meta:
        app_label = "property"
