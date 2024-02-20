from rest_framework import serializers
from ..models.user import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','email', 'mobile_number', 'name','is_verified','password')
        extra_kwargs = {'is_verified':{'read_only':True},
                        'id':{'read_only':True},
                        'password':{'write_only':True}
        }


    def create(self,validated_data):
        return CustomUser.objects.create_user(**validated_data)