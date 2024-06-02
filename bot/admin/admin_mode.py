from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message, Chat
from fluent.runtime import FluentLocalization

from bot.filters.admin import IsAdmin
from bot.utils.utils import extract_id
from db.base import db

# Initialize a new router
router_info = Router()

# Apply the IsAdmin filter to all messages handled by this router
router_info.message.filter(IsAdmin())


@router_info.message(Command("who"), F.reply_to_message)
async def get_user_info(message: Message, bot: Bot, l10n: FluentLocalization):
    """
    This function is an asynchronous function that gets the information of a user.
    It is triggered when the "who" command is sent in a message.

    Args:
        message (Message): The message object that triggered the command.
        bot (Bot): The bot instance.
        l10n (FluentLocalization): The localization instance.

    Returns:
        None
    """

    def get_full_name(chat: Chat):
        """
        This function gets the full name of a user from a chat object.

        Args:
            chat (Chat): The chat object.

        Returns:
            str: The full name of the user.
        """
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
        await message.reply(
            l10n.format_value(
                msg_id="cannot-get-user-info-error",
                args={"error": ex.message})
        )
        return

    u = f"@{user.username}" if user.username else "None"
    await message.reply(
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
    """
    This function is an asynchronous function that gets the list of all users.
    It is triggered when the "users" command is sent in a message.

    Args:
        message (Message): The message object that triggered the command.
        l10n (FluentLocalization): The localization instance.

    Returns:
        None
    """
    users = await db.get_users()
    if not users:
        return await message.reply(l10n.format_value("no-users-error"))
    users_str = "\n".join([f"{u}" for u in users])
    await message.reply(users_str)
