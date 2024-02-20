from django.db import models
from .post import Post
class PostImage(models.Model): 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to='API/images',max_length=100,null=True)


    class Meta:
        app_label = "posts"