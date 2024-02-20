from django.db import models
from .user import CustomUser
class OTP(models.Model): 
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    otp_number = models.PositiveIntegerField()


    def __str__(self) -> str:
        return f'{self.user.name} OPT {self.otp_number}'
    class Meta:
        app_label = "accounts"