from ninja import Schema

from modules.auth_service.services.v1.user.update.verify.dto.input.update import CheckVerifyInputDTO


class VerifyTokenSchema(Schema):
    token: str

    def to_dto(self) -> "CheckVerifyInputDTO":
        return CheckVerifyInputDTO(token=self.token)
