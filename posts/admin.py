from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models.post import Post
from .models.post_image import PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


class PostResource(resources.ModelResource):
    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "content",
            "purpose",
            "property_type",
            "price",
            "area_formating",
            "area1",
            "area2",
            "area3",
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
            "latitude",
            "longitude",
        )


@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    resource_class = PostResource
    inlines = (PostImageInline,)
    list_display = (
        "title",
        "property_type",
        "purpose",
        "city",
        "price",
        "author",
        "created_at",
    )
    list_filter = ("property_type", "purpose", "city", "area_formating")
    search_fields = ("title", "location", "city", "author__email")
    list_select_related = ("author",)
    date_hierarchy = "created_at"


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "images", "uploaded_at")
