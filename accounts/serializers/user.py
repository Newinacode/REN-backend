import re

from rest_framework import serializers

from ..models.user import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "mobile_number",
            "name",
            "is_verified",
            "password",
        )
        read_only_fields = ("id", "is_verified")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_mobile_number(self, value):
        digits = re.sub(r"\D", "", value or "")
        if len(digits) != 10:
            raise serializers.ValidationError(
                "Enter a valid 10 digit mobile number."
            )
        return digits

    def validate_email(self, value):
        return value.strip().lower()

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
