from django.db import models
from .property import Property

'''
Land Model 
inheritance: Property Model(Base Model)
'''

class Land(Property): 
    property_type = models.CharField(default="L",max_length=1)


    class Meta:
        app_label = "property"

