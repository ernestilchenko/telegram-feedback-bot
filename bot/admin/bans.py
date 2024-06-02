from aiogram import Router, F
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from bot.filters.admin import IsAdmin
from bot.utils.utils import extract_id
from db.base import db

# Initialize a new router
router_bans = Router()

# Apply the IsAdmin filter to all messages handled by this router
router_bans.message.filter(IsAdmin())

@router_bans.message(Command("ban"), F.reply_to_message)
async def cmd_ban(message: Message, l10n: FluentLocalization):
    """
    This function is an asynchronous function that bans a user.
    It is triggered when the "ban" command is sent in a message.

    Args:
        message (Message): The message object that triggered the command.
        l10n (FluentLocalization): The localization instance.

    Returns:
        None
    """
    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))
    await db.bun_user(int(user_id))
    await message.reply(
        l10n.format_value(
            msg_id="user-banned",
            args={"id": user_id}
        )
    )

@router_bans.message(Command("unban"), F.reply_to_message)
async def cmd_unban(message: Message, l10n: FluentLocalization):
    """
    This function is an asynchronous function that unbans a user.
    It is triggered when the "unban" command is sent in a message.

    Args:
        message (Message): The message object that triggered the command.
        l10n (FluentLocalization): The localization instance.

    Returns:
        None
    """
    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))
    user_id = int(user_id)
    await db.unban_user(user_id)
    await message.reply(
        l10n.format_value(
            msg_id="user-unbanned",
            args={"id": user_id}
        )
    )

@router_bans.message(F.reply_to_message)
async def reply_to_user(message: Message, l10n: FluentLocalization):
    """
    This function is an asynchronous function that replies to a user.
    It is triggered when a message is replied to.

    Args:
        message (Message): The message object that triggered the command.
        l10n (FluentLocalization): The localization instance.

    Returns:
        None
    """
    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))
    try:
        await message.copy_to(user_id)
    except TelegramAPIError as ex:
        await message.reply(
            l10n.format_value(
                msg_id="cannot-answer-to-user-error",
                args={"error": ex.message})
        )