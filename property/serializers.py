from rest_framework import serializers
from .models import House,Land,Property


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        abstract = True
        # extra_kwargs ={"post":{"required":False,"allow_null":False}}

class HouseSerializer(PropertySerializer):
    class Meta(PropertySerializer.Meta):
        model = House
        fields = '__all__'

class LandSerializer(PropertySerializer):
    class Meta(PropertySerializer.Meta):
        model = Land
        fields = '__all__'
