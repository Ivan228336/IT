from modules.auth_service.services.v1.token.update.dto.input.update import UpdateTokenInputDTO
from modules.auth_service.services.v1.token.update.dto.output.update import (
    UpdateTokenOutputDTO,
    UpdateTokenOutputDTOError,
    UpdateTokenOutputDTOSuccess,
)
from modules.auth_service.utils.token import JWTTokens


class UpdateTokensService:
    @staticmethod
    def update_tokens(dto: UpdateTokenInputDTO) -> tuple[int, UpdateTokenOutputDTO]:
        if not dto.refresh:
            return 400, UpdateTokenOutputDTOError(error="token is empty", detail="Refresh token is required")
        jwt_tokens = JWTTokens()
        status, result = jwt_tokens.update_tokens(dto.refresh)
        if status != 200:
            return status, UpdateTokenOutputDTOError.from_result(result)
        return status, UpdateTokenOutputDTOSuccess.from_result(result)
