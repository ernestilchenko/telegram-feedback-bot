from asyncio import sleep

from aiogram.types import Message
from fluent.runtime import FluentLocalization


async def send_notification(message: Message, message_id: int, l10n: FluentLocalization) -> None:
    await message.reply(l10n.format_value("sent-confirmation"), reply=False)
    await sleep(5.0)
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message_id)


def extract_id(message: Message) -> int:
    entities = message.entities or message.caption_entities
    if not entities or entities[-1].type != "hashtag":
        raise ValueError("There is a missing ID for the reply!")
    hashtag = entities[-1].extract_from(message.text or message.caption)
    if len(hashtag) < 4 or not hashtag[3:].isdigit():
        raise ValueError("Incorrect ID for the reply!")
    return int(hashtag[3:])
