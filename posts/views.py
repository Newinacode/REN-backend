from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer,MapSerializer
from rest_framework import mixins,generics,viewsets,serializers
from property.serializers import HouseSerializer,LandSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication



class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    # def perform_create(self, serializer):
    #     house_data = dict(self.request.data).pop('house', None)
    #     land_data = dict(self.request.data).pop('land', None)
    #     map_data = dict(self.request.data).pop('map', None)
        
    #     post = serializer.save()
        
    #     house_serializer = HouseSerializer(data=house_data)
    #     land_serializer = LandSerializer(data=land_data)
    #     map_serializer = MapSerializer(data=map_data)
        
    #     if house_serializer.is_valid() and land_serializer.is_valid() and map_serializer.is_valid():
    #         house = house_serializer.save()
    #         land = land_serializer.save()
    #         map = map_serializer.save()
            
    #         post.house = house
    #         post.land = land
    #         post.map = map
    #         post.save()
    #     else:
    #         raise serializers.ValidationError(house_serializer.errors)





    







    






