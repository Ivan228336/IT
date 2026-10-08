from typing import Any

import jwt
from django.core.cache import InvalidCacheBackendError
from redis.exceptions import RedisError

from modules.auth_service.services.v1.token.delete.dto.input.delete import LogoutInputDTO
from modules.auth_service.utils.token import JWTTokens


class LogoutService:
    @staticmethod
    def user_logout(dto: LogoutInputDTO) -> tuple[int, dict[str, Any]]:
        jwt_tokens = JWTTokens()
        try:
            if jwt_tokens.check_pair_tokens(dto.access_token, dto.refresh_token):
                return 200, {"success": True, "message": "Logout was successfully"}

            return 400, {"error": "invalid tokens"}

        except ConnectionError as e:
            return 500, {"error": "connection error", "detail": str(e)}

        except RedisError as e:
            return 500, {"error": "redis error", "detail": str(e)}

        except InvalidCacheBackendError as e:
            return 401, {"error": "invalid cache backend", "detail": str(e)}

        except jwt.InvalidTokenError as e:
            return 401, {"error": "invalid_token", "detail": str(e)}

        except Exception as e:
            return 500, {"error": "unknown error", "detail": str(e)}
