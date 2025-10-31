import logging

from aiogram import Router, Bot, F
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Chat, Message
from fluent.runtime import FluentLocalization

from bot.filters.admin import IsAdmin
from db.base import db

logger = logging.getLogger(__name__)

router_callbacks = Router()
router_callbacks.callback_query.filter(IsAdmin())


class ReplyState(StatesGroup):
    waiting_for_reply = State()


@router_callbacks.callback_query(F.data.startswith("info:"))
async def callback_info(callback: CallbackQuery, bot: Bot, l10n: FluentLocalization):
    user_id = int(callback.data.split(":")[1])

    def get_full_name(chat: Chat):
        if not chat.first_name:
            return ""
        if not chat.last_name:
            return chat.first_name
        return f"{chat.first_name} {chat.last_name}"

    try:
        user = await bot.get_chat(user_id)
    except TelegramAPIError as ex:
        logger.error(f"Failed to get user info for {user_id}: {ex.message}")
        return await callback.answer(
            l10n.format_value(
                msg_id="cannot-get-user-info-error",
                args={"error": ex.message}
            ),
            show_alert=True
        )

    u = f"@{user.username}" if user.username else "None"
    info_text = l10n.format_value(
        msg_id="user-info",
        args={
            "name": get_full_name(user),
            "id": user.id,
            "username": u
        }
    )
    await callback.answer(info_text, show_alert=True)


@router_callbacks.callback_query(F.data.startswith("ban:"))
async def callback_ban(callback: CallbackQuery, l10n: FluentLocalization):
    user_id = int(callback.data.split(":")[1])
    await db.bun_user(user_id)
    await callback.answer(
        l10n.format_value(
            msg_id="user-banned",
            args={"id": user_id}
        ),
        show_alert=True
    )


@router_callbacks.callback_query(F.data.startswith("unban:"))
async def callback_unban(callback: CallbackQuery, l10n: FluentLocalization):
    user_id = int(callback.data.split(":")[1])
    await db.unban_user(user_id)
    await callback.answer(
        l10n.format_value(
            msg_id="user-unbanned",
            args={"id": user_id}
        ),
        show_alert=True
    )


@router_callbacks.callback_query(F.data.startswith("reply:"))
async def callback_reply(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(":")[1])
    await state.set_state(ReplyState.waiting_for_reply)
    await state.update_data(target_user_id=user_id)
    await callback.answer()
    await callback.message.reply("Send your reply message:")


@router_callbacks.message(ReplyState.waiting_for_reply)
async def process_reply(message: Message, state: FSMContext, l10n: FluentLocalization):
    data = await state.get_data()
    user_id = data.get("target_user_id")

    try:
        await message.copy_to(user_id)
        await message.reply("✅ Message sent")
    except TelegramAPIError as ex:
        await message.reply(
            l10n.format_value(
                msg_id="cannot-answer-to-user-error",
                args={"error": ex.message}
            )
        )

    await state.clear()
