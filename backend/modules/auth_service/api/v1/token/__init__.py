from ninja import Router

from .create.authorization import router as is_create
from .delete.logout import router as is_delete
from .update.update import router as is_update

token_router = Router()

token_router.add_router("", is_update)
token_router.add_router("", is_delete)
token_router.add_router("", is_create)

__all__ = ("token_router",)
