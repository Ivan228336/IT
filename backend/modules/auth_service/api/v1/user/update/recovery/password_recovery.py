from django.http import HttpRequest
from ninja import Status

from modules.auth_service.api.v1.user.update.recovery.schemes.input.update import RecoveryPassSchema
from modules.auth_service.services.v1.user.update.recovery.password_recovery import PasswordRecoveryService
from modules.core.schemas.response_schemas import ErrorResponse, SuccessResponse

from ...router import auth_user_router_general as router


@router.post(
    "/recovery_pass", response={200: SuccessResponse, 400: ErrorResponse, 401: ErrorResponse, 500: ErrorResponse}
)
def recovery_password(request: HttpRequest, payload: RecoveryPassSchema) -> Status:
    """Восстановления пароля."""
    return Status(*PasswordRecoveryService.recovery_password(payload.to_dto()))
