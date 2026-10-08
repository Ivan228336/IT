from typing import Any

import jwt
from django.contrib.auth import get_user_model

from config.settings import settings
from modules.auth_service.repositories.v1.user.update.verify.check_verify import CheckVerifyRepository
from modules.auth_service.services.v1.user.update.verify.dto.input.update import CheckVerifyInputDTO
from modules.auth_service.utils.token import JWTTokens

User = get_user_model()


class CheckVerifyService:
    @staticmethod
    def verify(dto: CheckVerifyInputDTO) -> tuple[int, dict[str, Any]]:
        try:
            payload = jwt.decode(dto.token, settings.SECRET_KEY, algorithms=["HS256"])

            user = CheckVerifyRepository.make_user_active(payload["user_id"])

            jwt_tokens = JWTTokens()
            access_token, access_exp = jwt_tokens.create_access_token(str(user.id))
            if access_token is None or access_exp is None:
                return 500, {
                    "error": "access_token_creation_failed",
                    "detail": "Не удалось создать access токен. Попробуйте позже.",
                }
            refresh_token, refresh_exp = jwt_tokens.create_refresh_token(str(user.id))
            if refresh_token is None or refresh_exp is None:
                return 500, {
                    "error": "refresh_token_creation_failed",
                    "detail": "Не удалось создать refresh токен. Попробуйте позже.",
                }

            return 200, {
                "success": True,
                "message": "Email confirmed",
                "access": access_token,
                "refresh": refresh_token,
                "access_exp": access_exp,
                "refresh_exp": refresh_exp,
            }

        except jwt.ExpiredSignatureError:
            return 400, {"error": "Ссылка устарела"}
        except jwt.InvalidTokenError:
            return 400, {"error": "Недействительная ссылка"}
        except User.DoesNotExist:
            return 404, {"error": "Пользователь не найден"}
