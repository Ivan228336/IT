from ninja import Field, Schema
from pydantic import field_validator


class EmailSchema(Schema):
    email: str = Field(
        max_length=255,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9]@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        examples=["user@example.com", "john.doe@company.co.uk"],
        description=(
            "Email. Имя пользователя: латинские буквы, цифры, ., -, _\nДоменное имя: стандартное доменное имя"
        ),
    )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """Приводим email к нижнему регистру."""
        return v.strip().lower()
