from rest_framework import serializers
from ..models.property import Property
from ..models.house import House
from ..models.land import Land
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        abstract = True
        # extra_kwargs ={"post":{"required":False,"allow_null":False}}