from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from ..managers.usermanager import CustomUserManager

class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    mobile_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number', 'name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Only admin accounts can use Django's permission system."""
        return self.is_active and self.is_admin

    def has_module_perms(self, app_label):
        """Only admin accounts can access app modules in the admin."""
        return self.is_active and self.is_admin

    @property
    def is_staff(self):
        """Admin accounts are the only staff accounts."""
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin
        
    class Meta:
        app_label = "accounts"



