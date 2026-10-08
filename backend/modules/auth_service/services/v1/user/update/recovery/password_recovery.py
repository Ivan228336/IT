from typing import Any

from django.contrib.auth import get_user_model
from django.db import DatabaseError

from modules.auth_service.repositories.v1.user.update.recovery.password_recovery import (
    PasswordRecoveryResponseRepository,
)
from modules.auth_service.services.v1.user.update.recovery.dto.input.update import PasswordRecoveryInputDTO
from modules.auth_service.utils.send import SendEmailTask
from modules.core.utils.generate_pass import generate_password

User = get_user_model()


class PasswordRecoveryService:
    @staticmethod
    def recovery_password(dto: PasswordRecoveryInputDTO) -> tuple[int, dict[str, Any]]:
        if not PasswordRecoveryResponseRepository.user_exists(dto.email):
            return 400, {"error": f"User with email {dto.email} does not exist"}

        user = PasswordRecoveryResponseRepository.get_user_by_email(dto.email)
        try:
            new_password = generate_password()
            try:
                PasswordRecoveryResponseRepository.set_user_password(user, new_password)
            except DatabaseError:
                return 500, {"error": "Database error", "detail": "Could not create user"}

            SendEmailTask.async_send(dto.email, new_password)
            return 200, {"success": True, "message": "Password sent"}
        except Exception as e:
            return 400, {"error": f"Error {e}"}
