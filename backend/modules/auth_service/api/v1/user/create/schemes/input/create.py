from ninja import Field, Schema
from pydantic import field_validator, model_validator

from modules.auth_service.services.v1.user.create.dto.input.create import RegisterUserInputDTO
from modules.auth_service.utils.validators import validate_password, validate_username


class UserRegistrationSchemaIn(Schema):
    """Схема валидации данных для регистрации нового пользователя."""

    username: str = Field(max_length=30, description="Никнейм")

    email: str = Field(
        max_length=255,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9]@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        examples=["user@example.com", "john.doe@company.co.uk"],
        description=(
            "Email. Имя пользователя: латинские буквы, цифры, ., -, _\nДоменное имя: стандартное доменное имя"
        ),
    )

    password: str = Field(
        min_length=8,
        max_length=128,
        description=(
            "Пароль 8-128 символов. Требования:\n"
            "• Заглавные и строчные латинские буквы\n"
            "• Цифры\n"
            "• Спецсимволы: ~!@#%^&*_-+=`|\\(){}[]:;\"'<>,.?/$\n"
            "• Без символов валют"
        ),
        json_schema_extra={"writeOnly": True},
    )

    confirm_password: str = Field(
        min_length=8, max_length=128, description="Подтверждение пароля", json_schema_extra={"writeOnly": True}
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        return validate_username(v)

    @field_validator("password", "confirm_password")
    @classmethod
    def validate_password_fields(cls, v: str) -> str:
        """Валидация пароля и подтверждения пароля."""
        return validate_password(v)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """Приводим email к нижнему регистру."""
        return v.strip().lower()

    @model_validator(mode="after")
    def validate_passwords_match(self) -> "UserRegistrationSchemaIn":
        """Проверяет, совпадают ли password и confirm_password."""
        if self.password != self.confirm_password:
            raise ValueError("Пароли не совпадают")
        return self

    def to_dto(self) -> RegisterUserInputDTO:
        return RegisterUserInputDTO(username=self.username, email=self.email, password=self.password)
