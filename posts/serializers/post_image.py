from rest_framework import serializers

from ..models.post_image import PostImage


class PostImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PostImage
        fields = ("id", "images", "image_url", "post")
        read_only_fields = ("post",)

    def get_image_url(self, obj):
        if not obj.images:
            return None
        url = obj.images.url
        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(url)
        return url
