from django.db import models
from django.utils import timezone

from accounts.models.user import CustomUser
from posts.models.post import Post


class SavedHome(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="saved_homes"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="saved_by"
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "users"
        unique_together = ("user", "post")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user} saved {self.post}"
