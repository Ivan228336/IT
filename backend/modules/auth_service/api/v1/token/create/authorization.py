from django.contrib.auth import authenticate
from django.http import HttpRequest
from ninja import Status

from modules.auth_service.services.v1.token.create.authorization import AuthService
from modules.auth_service.services.v1.token.create.dto.input.create import AuthInputDTO
from modules.core.schemas.response_schemas import ErrorResponse

from ..router import token_router_general as router
from .schemes.input.create import LoginSchemaIn
from .schemes.output.create import LoginSchemaOut, Mapper


@router.post(
    "/authorization", response={200: LoginSchemaOut, 401: ErrorResponse, 403: ErrorResponse, 500: ErrorResponse}
)
def authorization(request: HttpRequest, payload: LoginSchemaIn) -> Status:
    """Аутентификация пользователя и выдача JWT токенов."""
    user = authenticate(request, username=payload.email, password=payload.password)
    if not user:
        return Status(401, {"error": "user authorization failed", "detail": "User not exists/can`t authorization"})
    return Status(*Mapper.from_dto(*AuthService.user_auth(AuthInputDTO(user_id=user.id))))
