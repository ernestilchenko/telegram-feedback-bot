from aiogram.filters import BaseFilter
from aiogram.types import Message

from db.base import db


class IsAdmin(BaseFilter):
    """
    This class is a custom filter for aiogram that checks if a user is an admin.

    It inherits from the BaseFilter class provided by aiogram.

    The __call__ method is overridden to provide the custom filtering logic.
    """

    async def __call__(self, message: Message) -> bool:
        """
        This method is an asynchronous method that checks if the user who sent a message is an admin.

        It is called when the filter is applied to a message.

        Args:
            message (Message): The message object that is being filtered.

        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        # Get the list of admins from the database
        admins = await db.get_admins()

        # Check if the user who sent the message is in the list of admins
        return message.from_user.id in admins
