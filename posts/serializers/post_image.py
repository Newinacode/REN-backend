from rest_framework import serializers
from ..models.post_image import PostImage

class PostImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url',)
    

    class Meta:
        model = PostImage
        fields = ("id","images","image_url","post")
   
    def get_image_url(self, obj):
        return obj.images.urls