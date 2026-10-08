from ninja import Router
from .api.register import register_router
from .api.authorization import authorization_router
from .api.password_recovery import recovery_pass_router

auth_router = Router(tags=['Авторизация'])

register_router.tags = ["Авторизация"]
authorization_router.tags = ["Авторизация"]
recovery_pass_router.tags = ["Авторизация"]

auth_router.add_router('', register_router)
auth_router.add_router('', authorization_router)
auth_router.add_router('', recovery_pass_router)
