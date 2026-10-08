from ninja import Router

from .token import token_router
from .user import auth_user_router

auth_service_router = Router()

auth_service_router.add_router("", auth_user_router)
auth_service_router.add_router("", token_router)

__all__ = ("auth_service_router",)
