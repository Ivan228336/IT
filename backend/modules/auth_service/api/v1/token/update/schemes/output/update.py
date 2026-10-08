from ninja import Schema

from modules.auth_service.services.v1.token.update.dto.output.update import (
    UpdateTokenOutputDTO,
    UpdateTokenOutputDTOSuccess,
)
from modules.core.schemas.response_schemas import ErrorResponse


class UpdateTokensSchemaOut(Schema):
    success: bool
    access: str
    refresh: str
    access_exp: str
    refresh_exp: str

    @classmethod
    def from_dto(cls, dto: UpdateTokenOutputDTOSuccess) -> "UpdateTokensSchemaOut":
        return cls(
            success=dto.success,
            access=dto.access,
            refresh=dto.refresh,
            access_exp=dto.access_exp,
            refresh_exp=dto.refresh_exp,
        )


class Mapper:
    @staticmethod
    def from_dto(status: int, dto: UpdateTokenOutputDTO) -> tuple[int, UpdateTokensSchemaOut | ErrorResponse]:
        if status == 200:
            return status, UpdateTokensSchemaOut.from_dto(dto)
        return status, ErrorResponse(error=dto.error, detail=dto.detail)
