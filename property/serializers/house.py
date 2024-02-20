from .property import PropertySerializer
from ..models.house import House


class HouseSerializer(PropertySerializer):
    class Meta(PropertySerializer.Meta):
        model = House
        fields = '__all__'
