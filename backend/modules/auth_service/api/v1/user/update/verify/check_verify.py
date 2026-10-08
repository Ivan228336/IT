from typing import Any

from django.http import HttpRequest
from ninja import Status

from modules.auth_service.api.v1.user.update.verify.schemes.input.update import VerifyTokenSchema
from modules.auth_service.services.v1.user.update.verify.check_verify import CheckVerifyService
from modules.core.schemas.response_schemas import ErrorResponse

from ...router import auth_user_router_general as router


@router.post("/verify", response={200: dict[str, Any], 400: ErrorResponse, 404: ErrorResponse, 500: ErrorResponse})
def check_verify(request: HttpRequest, payload: VerifyTokenSchema) -> Status:
    """Подтверждение email пользователя по верификационному токену."""
    return Status(*CheckVerifyService.verify(payload.to_dto()))
