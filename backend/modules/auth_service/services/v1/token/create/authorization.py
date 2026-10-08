from modules.auth_service.services.v1.token.create.dto.input.create import AuthInputDTO
from modules.auth_service.services.v1.token.create.dto.output.create import AuthOutputDTOError, AuthOutputDTOSuccess
from modules.auth_service.utils.token import JWTTokens


class AuthService:
    @staticmethod
    def user_auth(dto: AuthInputDTO) -> tuple[int, AuthOutputDTOSuccess | AuthOutputDTOError]:
        jwt_tokens = JWTTokens()
        status, result = jwt_tokens.create_tokens(dto.user_id)

        if status != 200:
            return status, AuthOutputDTOError.from_result(result)

        return 200, AuthOutputDTOSuccess.from_result(result)
