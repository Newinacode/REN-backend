from rest_framework import serializers
from ..models.post import Post
from property.serializers.house import HouseSerializer


from rest_framework.permissions import IsAuthenticated
from ..serializers.post_image import PostImageSerializer
class PostSerializer(HouseSerializer,serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    images = PostImageSerializer(many=True,required=False)

    class Meta: 
        model = Post
        fields ='__all__'