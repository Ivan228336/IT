from ninja import Schema

from modules.auth_service.services.v1.token.create.dto.output.create import AuthOutputDTO, AuthOutputDTOSuccess
from modules.core.schemas.response_schemas import ErrorResponse


class LoginSchemaOut(Schema):
    success: bool
    access: str
    refresh: str
    access_exp: str
    refresh_exp: str

    @classmethod
    def from_dto(cls, dto: AuthOutputDTOSuccess) -> "LoginSchemaOut":
        return cls(
            success=dto.success,
            access=dto.access,
            refresh=dto.refresh,
            access_exp=dto.access_exp,
            refresh_exp=dto.refresh_exp,
        )


class Mapper:
    @staticmethod
    def from_dto(status: int, dto: AuthOutputDTO) -> tuple[int, LoginSchemaOut | ErrorResponse]:
        if status == 200:
            return status, LoginSchemaOut.from_dto(dto)
        return status, ErrorResponse(error=dto.error, detail=dto.detail)
