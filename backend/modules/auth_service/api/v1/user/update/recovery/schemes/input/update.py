from ninja import Field, Schema
from pydantic import field_validator

from modules.auth_service.services.v1.user.update.recovery.dto.input.update import PasswordRecoveryInputDTO
from modules.auth_service.utils.validators import normalize_and_validate_email


class RecoveryPassSchema(Schema):
    email: str = Field(max_length=255, examples=["user@example.com"], description="Email для входа в систему")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Приводим email к нижнему регистру и проверяем на соответствие паттерну."""
        return normalize_and_validate_email(v)

    def to_dto(self) -> PasswordRecoveryInputDTO:
        return PasswordRecoveryInputDTO(email=self.email)
