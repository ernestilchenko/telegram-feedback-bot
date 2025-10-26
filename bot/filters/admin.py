from aiogram.filters import BaseFilter
from aiogram.types import Message

from db.base import db


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        admins = await db.get_admins()
        return message.from_user.id in admins
