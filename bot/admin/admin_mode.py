from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message, Chat
from fluent.runtime import FluentLocalization

from bot.filters.admin import IsAdmin
from bot.utils.utils import extract_id
from db.base import db

router_info = Router()
router_info.message.filter(IsAdmin())


@router_info.message(Command("who"), F.reply_to_message)
async def get_user_info(message: Message, bot: Bot, l10n: FluentLocalization):
    def get_full_name(chat: Chat):
        if not chat.first_name:
            return ""
        if not chat.last_name:
            return chat.first_name
        return f"{chat.first_name} {chat.last_name}"

    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))

    try:
        user = await bot.get_chat(user_id)
    except TelegramAPIError as ex:
        return await message.reply(
            l10n.format_value(
                msg_id="cannot-get-user-info-error",
                args={"error": ex.message})
        )

    u = f"@{user.username}" if user.username else "None"
    return await message.reply(
        l10n.format_value(
            msg_id="user-info",
            args={
                "name": get_full_name(user),
                "id": user.id,
                "username": u
            }
        )
    )


@router_info.message(Command("users"))
async def get_users(message: Message, l10n: FluentLocalization):
    users = await db.get_users()
    if not users:
        return await message.reply(l10n.format_value("no-users-error"))
    users_str = "\n".join([f"{u}" for u in users])
    return await message.reply(users_str)