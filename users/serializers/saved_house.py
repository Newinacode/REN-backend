from rest_framework import serializers

from ..models.saved_house import SavedHome


class SavedHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedHome
        fields = ("id", "user", "post", "created_at")
        read_only_fields = ("user", "post", "created_at")
