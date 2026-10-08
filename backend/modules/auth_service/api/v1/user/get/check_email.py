from django.http import HttpRequest
from ninja import Query, Status

from modules.auth_service.api.v1.user.get.schemes.input.get import EmailSchema
from modules.auth_service.api.v1.user.get.schemes.output.get import EmailAvailable
from modules.auth_service.utils.check_email import check_email as check_available_email
from modules.core.schemas.response_schemas import ErrorResponse

from ..router import auth_user_router_general as router


@router.get("/register/check-email", response={200: EmailAvailable, 409: EmailAvailable, 500: ErrorResponse})
def check_email(request: HttpRequest, payload: EmailSchema = Query(...)) -> Status:
    """Проверка email в реальном времени при регистрации."""
    if check_available_email(payload.email):
        return Status(200, EmailAvailable(message="Email is available", available=True, error=None))
    return Status(409, EmailAvailable(error="Email is not available", available=False, message=None))
