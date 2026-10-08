from ninja import Schema

from modules.auth_service.services.v1.token.update.dto.input.update import UpdateTokenInputDTO


class TokenSchemaIn(Schema):
    refresh: str

    def to_dto(self) -> UpdateTokenInputDTO:
        return UpdateTokenInputDTO(refresh=self.refresh)
