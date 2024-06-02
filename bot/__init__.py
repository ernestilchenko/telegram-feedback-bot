from aiogram import Router

from .admin.admin_mode import router_info
from .admin.bans import router_bans
from .handlers.usermode import router_user


def setup_routers() -> Router:
    router = Router()
    router.include_router(router_info)
    router.include_router(router_bans)
    router.include_router(router_user)
    return router
