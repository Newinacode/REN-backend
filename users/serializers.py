from rest_framework import serializers
from .models import SavedHome,Profile


class SavedHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedHome
        fields = '__all__'
        
     

