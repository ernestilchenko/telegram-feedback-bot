import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from bot.filters.admin import IsAdmin
from db.base import db

logger = logging.getLogger(__name__)

router_info = Router()
router_info.message.filter(IsAdmin())


@router_info.message(Command("users"))
async def get_users(message: Message, l10n: FluentLocalization):
    logger.info(f"Admin {message.from_user.id} requested users list")
    users = await db.get_users()
    if not users:
        return await message.reply(l10n.format_value("no-users-error"))
    users_str = "\n".join([f"{u}" for u in users])
    return await message.reply(users_str)
