import uuid
from datetime import UTC, datetime, timedelta

import jwt
from django.contrib.auth import get_user_model
from django.core.cache import InvalidCacheBackendError, caches
from django.db.utils import IntegrityError
from django.http import HttpRequest
from ninja.errors import AuthenticationError
from ninja.security import HttpBearer
from redis import RedisError

from config.settings import settings
from modules.auth_service.models.token import RefreshToken

REMAINING_REFRESH_TOKEN_TTL = 60 * 60 * 12

blacklist_cache = caches["blacklist"]


class JWTBearers(HttpBearer):
    """Аутентификация по JWT токену для Django Ninja."""

    def authenticate(self, request: HttpRequest, token: str):
        """Аутентификация пользователя по JWT токену."""
        try:
            jwt_tokens = JWTTokens()
            status, result = jwt_tokens.verify_access_token(token)
            if status == 200:
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"],
                )
                User = get_user_model()
                user = User.objects.get(id=payload.get("user_id"))
                if not user:
                    raise AuthenticationError("User not found")
                request.user = user
                return user
            elif status == 401 and result["error"] == "Token expired":
                request.token_expired = True
                request.token_error = result
                return None
            else:
                request.token_invalid = True
                request.token_error = result
                return None
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")
        except User.DoesNotExist:
            raise AuthenticationError("User not found")
        except Exception as e:
            raise AuthenticationError(f"Authentication failed: {str(e)}")


class JWTTokens:
    """Управление JWT токенами: создание, верификация, обновление."""

    def verify_access_token(self, token: str):
        """Проверяет access токен."""
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_nbf": True,
                    "verify_iat": True,
                    "require_exp": True,
                    "require_iat": True,
                },
            )

            if self.is_token_blacklisted(payload["jti"]):
                return 401, {"error": "Token revoked", "detail": "Access token has been revoked"}

            return 200, {"success": True, "message": "Token successfully verified"}
        except jwt.ExpiredSignatureError:
            return 401, {"error": "Token expired", "detail": "Token has expired"}
        except jwt.InvalidTokenError as e:
            return 401, {"error": "Invalid token", "detail": str(e)}

    def verify_refresh_token(self, token: str):
        """Проверяет refresh токен."""
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_nbf": False,
                    "verify_iat": True,
                    "require_exp": True,
                    "require_iat": True,
                },
            )

            if payload.get("token_type") != "refresh":
                return 401, {
                    "error": "Invalid token type",
                    "detail": "Expected refresh token, got {}".format(payload.get("token_type")),
                    "code": "wrong_token_type",
                }

            if "jti" not in payload:
                return 401, {
                    "error": "Invalid token structure",
                    "detail": "Refresh token missing jti field",
                    "code": "missing_jti",
                }

            if self.is_token_blacklisted(payload["jti"]):
                return 401, {
                    "error": "Token revoked",
                    "detail": "This refresh token has been revoked",
                    "code": "token_revoked",
                    "requires_login": True,
                }

            try:
                refresh_token = RefreshToken.objects.get(jti=payload["jti"], is_active=True)
            except RefreshToken.DoesNotExist:
                return 401, {
                    "error": "Token not found",
                    "detail": "Refresh token is not active or doesn't exist",
                    "code": "token_not_found",
                    "requires_login": True,
                }

            if str(refresh_token.user.id) != payload["user_id"]:
                return 401, {
                    "error": "Token validation failed",
                    "detail": "Token user mismatch",
                    "code": "user_mismatch",
                    "requires_login": True,
                }

            try:
                User = get_user_model()
                user = User.custom_object_auth_manager.get(id=int(payload["user_id"]))

                if not user.is_active:
                    return 401, {
                        "error": "User account disabled",
                        "detail": "User account has been deactivated",
                    }

            except User.DoesNotExist:
                return 401, {
                    "error": "User not found",
                    "detail": "User associated with this token no longer exists",
                }

            return 200, payload

        except jwt.ExpiredSignatureError:
            expired_payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False}
            )
            jti = expired_payload.get("jti")
            if jti:
                RefreshToken.objects.filter(jti=jti).update(is_active=False)

            return 401, {
                "error": "Refresh token expired",
                "detail": "Refresh token has expired, please login again",
            }

        except jwt.InvalidTokenError as e:
            return 401, {
                "error": "Invalid refresh token",
                "detail": str(e),
            }

    def create_tokens(self, user_id: int):
        """Создает access и refresh токены при логине."""
        access_token, access_exp = self.create_access_token(str(user_id))
        if access_token is None or access_exp is None:
            return 500, {
                "error": "access_token_creation_failed",
                "detail": "Не удалось создать access токен. Попробуйте позже.",
            }

        refresh_token, refresh_exp = self.create_refresh_token(str(user_id))
        if refresh_token is None or refresh_exp is None:
            return 500, {
                "error": "refresh_token_creation_failed",
                "detail": "Не удалось создать refresh токен. Попробуйте позже.",
            }

        return 200, {
            "success": True,
            "access": access_token,
            "refresh": refresh_token,
            "access_exp": access_exp,
            "refresh_exp": refresh_exp,
        }

    def create_access_token(self, user_id):
        """Создает access токен (15 минут)."""
        access_headers = {"type": "JWT"}
        access_payload = {
            "token_type": "access",
            "user_id": user_id,
            "exp": int((datetime.now(UTC) + timedelta(minutes=15)).timestamp()),
            "iat": int((datetime.now(UTC)).timestamp()),
            "jti": str(uuid.uuid4()),
        }

        access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256", headers=access_headers)

        return access_token, access_payload["exp"]

    def create_refresh_token(self, user_id):
        """Создает refresh токен (1 день) и сохраняет в БД."""
        exp = int((datetime.now(UTC) + timedelta(days=1)).timestamp())
        iat = int((datetime.now(UTC)).timestamp())
        jti = str(uuid.uuid4())

        refresh_headers = {"type": "JWT"}

        refresh_payload = {"token_type": "refresh", "user_id": user_id, "exp": exp, "iat": iat, "jti": jti}

        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256", headers=refresh_headers)
        try:
            User = get_user_model()
            user = User.custom_object_auth_manager.get(id=int(user_id))
        except User.DoesNotExist:
            return None, None

        try:
            RefreshToken.objects.create(jti=jti, user=user, is_active=True)
        except IntegrityError:
            return None, None

        return refresh_token, refresh_payload["exp"]

    def update_tokens(self, refresh_token: str):
        """Обновляет пару токенов. Ротирует refresh токен если истекает через 12 часов."""
        status, payload = self.verify_refresh_token(refresh_token)
        if status != 200:
            return status, {
                "error": payload.get("error", "invalid_refresh"),
                "detail": payload.get("detail", "Невалидный refresh токен"),
            }
        refresh_exp = payload["exp"]
        try:
            if refresh_exp - int((datetime.now(UTC)).timestamp()) <= REMAINING_REFRESH_TOKEN_TTL:
                RefreshToken.objects.filter(jti=payload["jti"]).update(is_active=False)
                refresh_token, refresh_exp = self.create_refresh_token(payload["user_id"])

                if refresh_token is None or refresh_exp is None:
                    return 500, {
                        "error": "refresh_token_creation_failed",
                        "detail": "Не удалось создать refresh токен. Попробуйте позже.",
                    }

            access_token, access_exp = self.create_access_token(payload["user_id"])

            if access_token is None or access_exp is None:
                return 500, {
                    "error": "access_token_creation_failed",
                    "detail": "Не удалось создать access токен. Попробуйте позже.",
                }

            return 200, {
                "success": True,
                "access": access_token,
                "refresh": refresh_token,
                "access_exp": access_exp,
                "refresh_exp": refresh_exp,
            }

        except (jwt.InvalidTokenError, jwt.DecodeError, jwt.ExpiredSignatureError) as e:
            return 500, {
                "error": "jwt_error",
                "detail": f"Ошибка обработки токена: {str(e)}",
            }
        except (KeyError, ValueError, TypeError) as e:
            return 500, {
                "error": "data_error",
                "detail": f"Некорректные данные токена: {str(e)}",
            }

    def is_token_blacklisted(self, jti: str) -> bool:
        """Проверяет, есть ли токен в черном списке по jti."""
        try:
            blacklist_key = f"blacklist:jti:{jti}"
            return blacklist_cache.get(blacklist_key) is not None

        except Exception as e:
            print(f"Unexpected error in is_token_blacklisted for jti {jti}: {type(e).__name__}: {e}")
            return False

    def blacklist_token(self, jti: str, ttl) -> bool:
        if self.is_token_blacklisted(jti):
            return True

        blacklist_key = f"blacklist:jti:{jti}"
        blacklist_cache.set(blacklist_key, "1", timeout=ttl)
        return True

    def check_pair_tokens(self, access_token: str, refresh_token: str) -> bool:
        try:
            refresh_payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False}
            )
            access_token_payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False}
            )
        except jwt.InvalidTokenError as e:
            raise e

        if not (refresh_payload["user_id"] == access_token_payload["user_id"]):
            return False

        refresh_jti = refresh_payload.get("jti")
        access_jti = access_token_payload.get("jti")

        refresh_exp = refresh_payload.get("exp", 0)
        access_exp = access_token_payload.get("exp", 0)

        refresh_ttl = max(0, int(refresh_exp - datetime.now().timestamp()))
        access_ttl = max(0, int(access_exp - datetime.now().timestamp()))

        if refresh_ttl > 0 and access_ttl > 0:
            try:
                refresh = self.blacklist_token(refresh_jti, refresh_ttl)
                access = self.blacklist_token(access_jti, access_ttl)

                return refresh and access

            except (ConnectionError, RedisError, InvalidCacheBackendError) as e:
                raise e

            except Exception as e:
                raise e
        else:
            return True
