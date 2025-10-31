from aiogram import Router

from .admin.admin_mode import router_info
from .admin.callbacks import router_callbacks
from .handlers.usermode import router_user


def setup_routers() -> Router:
    router = Router()
    router.include_router(router_info)
    router.include_router(router_callbacks)
    router.include_router(router_user)
    return router
