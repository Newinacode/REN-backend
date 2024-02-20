
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, mobile_number, name, password):
        """
        Creates and saves a user with the given email, mobile number, name, and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not mobile_number:
            raise ValueError("Users must have a mobile number")
        if not name:
            raise ValueError("Users must have a name")
        if not password: 
            raise ValueError("Users must have a password")

        user = self.model(
            email=self.normalize_email(email),
            mobile_number=mobile_number,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile_number, name, password):
        """
        Creates and saves a superuser with the given email, mobile number, name, and password.
        """
        user = self.create_user(
            email,
            mobile_number=mobile_number,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
