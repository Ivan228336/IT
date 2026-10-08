from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserAuthServiceManager(BaseUserManager["UserAuthServiceModel"]):
    def create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email, and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a Superuser with the given email, and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, password, **extra_fields)


class UserAuthServiceModel(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        unique=True,
    )
    username = models.CharField(
        max_length=30,
        unique=True,
    )

    custom_object_auth_manager = CustomUserAuthServiceManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        abstract = True
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
