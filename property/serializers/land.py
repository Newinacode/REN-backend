from .property import PropertySerializer
from ..models.land import Land


class LandSerializer(PropertySerializer):
    class Meta(PropertySerializer.Meta):
        model = Land
        fields = '__all__'
