from rest_framework import serializers
from ..models.saved_house import SavedHome


class SavedHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedHome
        fields = '__all__'
        
     