from ninja import Field, Schema
from pydantic import field_validator

from modules.auth_service.utils.validators import validate_password


class LoginSchemaIn(Schema):
    """Схема валидации данных для авторизации пользователя."""

    email: str = Field(
        max_length=255,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9]@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        examples=["user@example.com"],
        description="Email для входа в систему",
    )

    password: str = Field(
        min_length=8, max_length=128, description="Пароль для входа", json_schema_extra={"writeOnly": True}
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password(v)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """Приводим email к нижнему регистру."""
        return v.strip().lower()
