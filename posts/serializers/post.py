from rest_framework import serializers

from ..models.post import Post
from .post_image import PostImageSerializer


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    author_name = serializers.CharField(source="author.name", read_only=True)
    author_email = serializers.EmailField(source="author.email", read_only=True)
    purpose_display = serializers.CharField(
        source="get_purpose_display", read_only=True
    )
    property_type_display = serializers.CharField(
        source="get_property_type_display", read_only=True
    )
    area_display = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "author_name",
            "author_email",
            "title",
            "content",
            "purpose",
            "purpose_display",
            "property_type",
            "property_type_display",
            "price",
            "area_formating",
            "area1",
            "area2",
            "area3",
            "area_display",
            "road_width",
            "no_of_bedrooms",
            "no_of_bathrooms",
            "no_of_floor",
            "parking_area",
            "facing_side",
            "built_date",
            "street",
            "location",
            "city",
            "longitude",
            "latitude",
            "created_at",
            "updated_at",
            "images",
        )
        read_only_fields = ("author", "created_at", "updated_at", "images")
        extra_kwargs = {
            "title": {"required": True},
            "content": {"required": True},
            "location": {"required": True},
            "city": {"required": True},
            "longitude": {"min_value": -180, "max_value": 180},
            "latitude": {"min_value": -90, "max_value": 90},
        }

    def validate(self, attrs):
        property_type = attrs.get(
            "property_type", getattr(self.instance, "property_type", "H")
        )
        if property_type == Post.PropertyType.LAND:
            # Land listings do not have rooms; ignore stray values.
            for field in (
                "no_of_bedrooms",
                "no_of_bathrooms",
                "no_of_floor",
                "parking_area",
                "facing_side",
            ):
                attrs.setdefault(field, 0 if field != "facing_side" else "")
        return attrs
