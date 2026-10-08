from django.http import HttpRequest
from ninja import Status

from modules.auth_service.api.v1.user.create.schemes.input.create import UserRegistrationSchemaIn
from modules.auth_service.services.v1.user.create.register import RegisterUserService
from modules.core.schemas.response_schemas import ErrorResponse, SuccessResponse

from ..router import auth_user_router_general as router


@router.post("/register/", response={201: SuccessResponse, 400: ErrorResponse, 409: ErrorResponse, 500: ErrorResponse})
def register(request: HttpRequest, payload: UserRegistrationSchemaIn) -> Status:
    """Регистрация нового пользователя с отправкой подтверждения email."""
    return Status(*RegisterUserService.register_user(payload.to_dto()))
