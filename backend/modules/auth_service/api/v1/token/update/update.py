from django.http import HttpRequest
from ninja import Status

from modules.auth_service.api.v1.token.update.schemes.input.update import TokenSchemaIn
from modules.auth_service.api.v1.token.update.schemes.output.update import Mapper, UpdateTokensSchemaOut
from modules.auth_service.services.v1.token.update.update import UpdateTokensService
from modules.core.schemas.response_schemas import ErrorResponse

from ..router import token_router_general as router


@router.post(
    "/update_tokens", response={200: UpdateTokensSchemaOut, 400: ErrorResponse, 401: ErrorResponse, 500: ErrorResponse}
)
def update_jwt_tokens(request: HttpRequest, payload: TokenSchemaIn) -> Status:
    """Обновление пары JWT токенов по refresh токену."""
    return Status(*Mapper.from_dto(*UpdateTokensService.update_tokens(payload.to_dto())))
