from django.contrib.auth.models import BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from pydantic import BaseModel

from modules.auth_service.models import UserAuthServiceModel


def default_statistics():
    return {
        "created": {"places": 0, "events": 0, "routes": 0},
        "published": {"places": 0, "events": 0, "routes": 0},
        "visited": {"places": 0, "events": 0, "routes": 0},
    }


class CategoryStatisticsSchema(BaseModel):
    places: int = 0
    events: int = 0
    routes: int = 0


class UserStatisticsSchema(BaseModel):
    created: CategoryStatisticsSchema = CategoryStatisticsSchema()
    published: CategoryStatisticsSchema = CategoryStatisticsSchema()
    visited: CategoryStatisticsSchema = CategoryStatisticsSchema()

    def to_dict(self) -> dict:
        return self.model_dump()


class CustomUserAuthManager(BaseUserManager["User"]):
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


class User(UserAuthServiceModel):
    age = models.IntegerField(
        validators=[
            MinValueValidator(0, "Возраст не может быть отрицательным"),
            MaxValueValidator(99, "Максимальный возраст 99 лет"),
        ],
        blank=True,
        null=True,
        verbose_name="Возраст пользователя",
    )

    status = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        verbose_name="Статус пользователя",
    )

    statistics = models.JSONField(
        default=UserStatisticsSchema().to_dict,
        blank=True,
        verbose_name="Статистика пользователя",
    )

    photo = models.ImageField(blank=True, null=True, upload_to="users/photos/%Y/%m/%d/", verbose_name="Фото профиля")

    average_rating = models.FloatField(default=0, verbose_name="Рейтинг", max_length=5, blank=True, null=True)

    objects = CustomUserAuthManager()

    custom_object_auth_manager = CustomUserAuthManager()

    @property
    def statistics_schema(self) -> UserStatisticsSchema:
        return UserStatisticsSchema(**self.statistics)

    @statistics_schema.setter
    def statistics_schema(self, value: UserStatisticsSchema) -> None:
        self.statistics = value.model_dump()

    def __str__(self):
        return f"{self.email}"
