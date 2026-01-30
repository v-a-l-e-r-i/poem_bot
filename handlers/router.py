from aiogram import Router

from handlers.user.submission import router as user_router
from handlers.admin.panel import router_admin as panel_router
from handlers.admin.view_media import router_admin as media_router

from utils.logger import setup_logger

logger = setup_logger()

root_router = Router()

root_router.include_router(panel_router)
root_router.include_router(media_router)

root_router.include_router(user_router)

logger.info(f"Panel router loaded: {panel_router}")
logger.info(f"Media router loaded: {media_router}")
logger.info(f"User router loaded: {user_router}")