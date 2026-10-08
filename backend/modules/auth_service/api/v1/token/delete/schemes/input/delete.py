from ninja import Schema

from modules.auth_service.services.v1.token.delete.dto.input.delete import LogoutInputDTO


class LogoutSchemaIn(Schema):
    refresh: str

    def to_dto(self, access_token: str) -> LogoutInputDTO:
        return LogoutInputDTO(access_token=access_token, refresh_token=self.refresh)
