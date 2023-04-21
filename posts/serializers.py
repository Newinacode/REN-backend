from rest_framework import serializers
from posts.models import Post,Map
from property.serializers import PropertySerializer,HouseSerializer,LandSerializer
from rest_framework.permissions import IsAuthenticated


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'



class PostSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    
    map = MapSerializer()
    land = LandSerializer(required=False)
    house = HouseSerializer(required=False)
    class Meta:
        model = Post
        fields ="__all__"
        # fields = ('id', 'title', 'content', 'house', 'land', 'map')
        
    def create(self, validated_data):
        house_data = validated_data.pop('house', None)
        land_data = validated_data.pop('land', None)
        map_data = validated_data.pop('map', None)

        post = Post.objects.create(**validated_data)
        
        if house_data:
            house_data['post'] = post.id
            house_serializer = HouseSerializer(data=house_data)
            if house_serializer.is_valid():
                house_serializer.save()
            else:
                raise serializers.ValidationError(house_serializer.errors)

        if land_data:
            land_data['post'] = post.id
            land_serializer = LandSerializer(data=land_data)
            if land_serializer.is_valid():
                land_serializer.save()
            else:
                raise serializers.ValidationError(land_serializer.errors)

        if map_data:
            map_data['post'] = post.id
            map_serializer = MapSerializer(data=map_data)
            if map_serializer.is_valid():
                map_serializer.save()
            else:
                raise serializers.ValidationError(map_serializer.errors)

        return post
