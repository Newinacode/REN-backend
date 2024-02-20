from django.db import models
from accounts.models.user import CustomUser
from posts.models.post import Post


class SavedHome(models.Model): 
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self): 
        return f'{self.user} liked {self.post}'
