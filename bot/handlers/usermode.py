from asyncio import create_task

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from bot.filters.supported_media import SupportedMediaFilter
from bot.utils.utils import send_notification
from db.base import db

# Initialize a new router
router_user = Router()


@router_user.message(Command("start"))
async def cmd_start(message: Message, l10n: FluentLocalization):
    """
    This function is an asynchronous function that starts a conversation with a user.
    It is triggered when the "start" command is sent in a message.

    Args:
        message (Message): The message object that triggered the command.
        l10n (FluentLocalization): The localization instance.

    Returns:
        None
    """
    ban_users = await db.get_ban_users()
    if message.from_user.id in ban_users:
        return await message.answer(l10n.format_value("you-were-banned-error"))
    await db.add_user(message.from_user.id)
    await message.answer(l10n.format_value("cmd-start", args={"name": message.from_user.full_name}))


@router_user.message(F.text)
async def text_msg(message: Message, bot: Bot, l10n: FluentLocalization):
    """
    This function is an asynchronous function that handles text messages from a user.
    It is triggered when a text message is sent.

    Args:
        message (Message): The message object that triggered the command.
        bot (Bot): The bot instance.
        l10n (FluentLocalization): The localization instance.

    Returns:
        None
    """
    ban_users = await db.get_ban_users()
    if message.from_user.id in ban_users:
        return await message.reply(l10n.format_value("you-were-banned-error"))
    if len(message.text) > 4000:
        return await message.reply(l10n.format_value("too-long-text-error"))
    else:
        admins = await db.get_admins()
        for admin in admins:
            await bot.send_message(
                chat_id=admin,
                text=message.html_text + f"\n\n#id{message.from_user.id}",
                parse_mode="HTML"
            )
            await create_task(send_notification(message, message.message_id, l10n))


@router_user.message(SupportedMediaFilter())
async def media_msg(message: Message, l10n: FluentLocalization):
    """
    This function is an asynchronous function that handles media messages from a user.
    It is triggered when a media message is sent.

    Args:
        message (Message): The message object that triggered the command.
        l10n (FluentLocalization): The localization instance.

    Returns:
        None
    """
    ban_users = await db.get_ban_users()
    if message.from_user.id in ban_users:
        return await message.reply(l10n.format_value("banned-error"))
    if message.caption and len(message.caption) > 1000:
        return await message.reply(l10n.format_value("too-long-caption-error"))
    else:
        admins = await db.get_admins()
        for admin in admins:
            await message.copy_to(chat_id=admin,
                                  caption=((message.caption or "") + f"\n\n#id{message.from_user.id}\n"),
                                  parse_mode="HTML"
                                  )
            await create_task(send_notification(message, message.message_id, l10n))
