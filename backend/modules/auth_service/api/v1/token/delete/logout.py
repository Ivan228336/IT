from django.http import HttpRequest
from ninja import Status

from modules.auth_service.api.v1.token.delete.schemes.input.delete import LogoutSchemaIn
from modules.auth_service.services.v1.token.delete.logout import LogoutService
from modules.auth_service.utils.token import JWTBearers
from modules.core.schemas.response_schemas import ErrorResponse, SuccessResponse

from ..router import token_router_general as router


@router.post(
    "/logout",
    response={200: SuccessResponse, 400: ErrorResponse, 401: ErrorResponse, 500: ErrorResponse},
    auth=JWTBearers(),
)
def logout(request: HttpRequest, payload: LogoutSchemaIn) -> Status:
    """Эндпоинт логаута."""
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return Status(*LogoutService.user_logout(payload.to_dto(access_token)))
