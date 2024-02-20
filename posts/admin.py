from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models.post import Post
from .models.post_image import PostImage
from import_export import resources



admin.site.register(PostImage)



class PostResources(ImportExportModelAdmin):

    class Meta:
        model = Post


admin.site.register(Post,PostResources)