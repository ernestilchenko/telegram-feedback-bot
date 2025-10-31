from asyncio import create_task

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from fluent.runtime import FluentLocalization

from bot.filters.supported_media import SupportedMediaFilter
from bot.utils.utils import send_notification
from db.base import db

router_user = Router()


def get_admin_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="ℹ️ Info", callback_data=f"info:{user_id}"),
            InlineKeyboardButton(text="✏️ Reply", callback_data=f"reply:{user_id}"),
        ],
        [
            InlineKeyboardButton(text="🚫 Ban", callback_data=f"ban:{user_id}"),
            InlineKeyboardButton(text="✅ Unban", callback_data=f"unban:{user_id}"),
        ]
    ])


@router_user.message(Command("start"))
async def cmd_start(message: Message, l10n: FluentLocalization):
    ban_users = await db.get_ban_users()
    if message.from_user.id in ban_users:
        return await message.answer(l10n.format_value("you-were-banned-error"))
    await db.add_user(message.from_user.id)
    return await message.answer(l10n.format_value("cmd-start", args={"name": message.from_user.full_name}))


@router_user.message(F.text)
async def text_msg(message: Message, bot: Bot, l10n: FluentLocalization):
    ban_users = await db.get_ban_users()
    if message.from_user.id in ban_users:
        return await message.reply(l10n.format_value("you-were-banned-error"))
    if len(message.text) > 4000:
        return await message.reply(l10n.format_value("too-long-text-error"))

    admins = await db.get_admins()
    keyboard = get_admin_keyboard(message.from_user.id)
    for admin in admins:
        await bot.send_message(
            chat_id=admin,
            text=message.html_text + f"\n\n#id{message.from_user.id}",
            parse_mode="HTML",
            reply_markup=keyboard
        )
    await create_task(send_notification(message, message.message_id, l10n))


@router_user.message(SupportedMediaFilter())
async def media_msg(message: Message, l10n: FluentLocalization):
    ban_users = await db.get_ban_users()
    if message.from_user.id in ban_users:
        return await message.reply(l10n.format_value("you-were-banned-error"))
    if message.caption and len(message.caption) > 1000:
        return await message.reply(l10n.format_value("too-long-caption-error"))

    admins = await db.get_admins()
    for admin in admins:
        await message.copy_to(
            chat_id=admin,
            caption=((message.caption or "") + f"\n\n#id{message.from_user.id}\n"),
            parse_mode="HTML"
        )
    await create_task(send_notification(message, message.message_id, l10n))
