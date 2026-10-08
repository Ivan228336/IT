from ninja import Router

from .create.register import router as is_create
from .get.check_email import router as is_get
from .update.recovery.password_recovery import router as is_update_recovery
from .update.verify.check_verify import router as is_update_verify

auth_user_router = Router()

auth_user_router.add_router("", is_update_recovery)
auth_user_router.add_router("", is_update_verify)
auth_user_router.add_router("", is_create)
auth_user_router.add_router("", is_get)


__all__ = ("auth_user_router",)
