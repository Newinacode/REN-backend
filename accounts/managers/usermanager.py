from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, mobile_number, name, password=None, **extra_fields):
        """Create and save a regular user."""
        if not email:
            raise ValueError("Users must have an email address")
        if not mobile_number:
            raise ValueError("Users must have a mobile number")
        if not name:
            raise ValueError("Users must have a name")
        if not password:
            raise ValueError("Users must have a password")

        email = self.normalize_email(email).lower()
        user = self.model(
            email=email,
            mobile_number=mobile_number,
            name=name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, mobile_number, name, password=None, **extra_fields
    ):
        """Create and save an admin user."""
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_verified", True)
        return self.create_user(
            email,
            mobile_number=mobile_number,
            name=name,
            password=password,
            **extra_fields,
        )
