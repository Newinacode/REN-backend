from rest_framework import serializers
from posts.models import Post,PostImage#,Map
from property.serializers import PropertySerializer,HouseSerializer,LandSerializer
from rest_framework.permissions import IsAuthenticated


# class MapSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Map
#         fields = '__all__'

     
class PostImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = PostImage
        fields = ("id","images","image_url","post")

    def get_image_url(self, obj):
        return obj.images.url








class PostSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    images= PostImageSerializer(many=True, read_only = True,)
    # uploaded_images = serializers.ListField(
    #     child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False,write_only=True)
 
    # )


    class Meta: 
        fields ='__all__'





# class SearchResultSerializer(PostSerializer): 
#     radius = serializers.FloatField()


#     class Meta: 
#         fields = "__all__"
# "title",
# "content",
# "created_at",
# "updated_at",
# "purpose",
# "area_formating",
# "area1",
# "area2",
# "area3",
# "price",
# "property_type",
# "no_of_bedrooms",
# "no_of_bathrooms",
# "no_of_floor",
# "parking_area",
# "facing_side",
# "built_date",
# "location",
# "street",
# "city",
# "longitude",
# "latitude","image","uploaded_images"]



    



    # def create(self,validated_data): 
    #     print(validated_data)
    #     upload_images = validated_data.pop("uploaded_images")
    #     post = Post.objects.create(**validated_data)
    #     for image in upload_images:
    #         PostImage.objects.create(post=post,images=image)

    #     return post

    # map = MapSerializer(required=False)
    # land = LandSerializer(required=False)
    # house = HouseSerializer(required=False)
    class Meta:
        model = Post
        fields ="__all__"
        # fields = ('id', 'title', 'content', 'house', 'land', 'map')

    #     extra_kwargs = {
    #         'id': {'read_only': False},
    #         'slug': {'validators': []},
    #     }
        
    # def create(self, validated_data):
    #     house_data = validated_data.pop('house', None)
    #     land_data = validated_data.pop('land', None)
    #     map_data = validated_data.pop('map', None)

    #     post = Post.objects.create(**validated_data)
        
    #     if house_data:
    #         house_data['post'] = post.id
    #         house_serializer = HouseSerializer(data=house_data)
    #         if house_serializer.is_valid():
    #             house_serializer.save()
    #         else:
    #             raise serializers.ValidationError(house_serializer.errors)

    #     if land_data:
    #         land_data['post'] = post.id
    #         land_serializer = LandSerializer(data=land_data)
    #         if land_serializer.is_valid():
    #             land_serializer.save()
    #         else:
    #             raise serializers.ValidationError(land_serializer.errors)

    #     if map_data:
    #         map_data['post'] = post.id
    #         map_serializer = MapSerializer(data=map_data)
    #         if map_serializer.is_valid():
    #             map_serializer.save()
    #         else:
    #             raise serializers.ValidationError(map_serializer.errors)

    #     return post


    # def update(self, instance, validated_data):
    #     instance = Post.objects.get(id=instance)
    #     house_data = validated_data.pop("house", None)
    #     land_data = validated_data.pop("land", None)
    #     map_data = validated_data.pop("map", None)

    #     instance.title = validated_data.get("title", instance.title)
    #     instance.content = validated_data.get("content", instance.content)
    #     instance.author = validated_data.get("author", instance.author)
    #     instance.save()

    #     if house_data:
    #         if instance.house:
    #             house_serializer = HouseSerializer(instance.house, data=house_data)
    #         else:
    #             house_data["post"] = instance.id
    #             house_serializer = HouseSerializer(data=house_data)
    #         if house_serializer.is_valid():
    #             house_serializer.save()
    #         else:
    #             raise serializers.ValidationError(house_serializer.errors)
    #     elif instance.house:
    #         instance.house.delete()

    #     if land_data:
    #         if instance.land:
    #             land_serializer = LandSerializer(instance.land, data=land_data)
    #         else:
    #             land_data["post"] = instance.id
    #             land_serializer = LandSerializer(data=land_data)
    #         if land_serializer.is_valid():
    #             land_serializer.save()
    #         else:
    #             raise serializers.ValidationError(land_serializer.errors)
    #     elif instance.land:
    #         instance.land.delete()

    #     if map_data:
    #         if instance.map:
    #             map_serializer = MapSerializer(instance.map, data=map_data)
    #         else:
    #             map_data["post"] = instance.id
    #             map_serializer = MapSerializer(data=map_data)
    #         if map_serializer.is_valid():
    #             map_serializer.save()
    #         else:
    #             raise serializers.ValidationError(map_serializer.errors)
    #     elif instance.map:
    #         instance.map.delete()

    #     return instance

