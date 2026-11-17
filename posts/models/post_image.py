from django.db import models
from django.utils import timezone

from .post import Post


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    images = models.ImageField(
        upload_to="properties/%Y/%m/", max_length=255, null=True, blank=True
    )
    uploaded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "posts"
        ordering = ["id"]

    def __str__(self) -> str:
        return f"Image #{self.pk} for {self.post.title}"
