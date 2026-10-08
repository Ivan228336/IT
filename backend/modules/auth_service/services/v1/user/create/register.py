from typing import Any

from django.db import DatabaseError

from modules.auth_service.repositories.v1.user.create.register import RegisterUserRepository
from modules.auth_service.services.v1.user.create.dto.input.create import RegisterUserInputDTO
from modules.auth_service.utils.send import SendEmailTask


class RegisterUserService:
    @staticmethod
    def register_user(dto: RegisterUserInputDTO) -> tuple[int, dict[str, Any]]:

        if RegisterUserRepository.check_email(dto.email):
            return 409, {"error": "Email is busy", "detail": "This email already used"}

        if RegisterUserRepository.check_username(dto.username):
            return 409, {"error": "Username is busy", "detail": "This username already used"}

        try:
            user = RegisterUserRepository.create_user(dto.username, dto.email, dto.password)
        except DatabaseError:
            return 500, {"error": "Database error", "detail": "Could not create user"}

        SendEmailTask.verify_by_email(user)

        return 201, {"success": True, "message": "User successfully created"}
