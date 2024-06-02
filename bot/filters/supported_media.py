from aiogram.filters import BaseFilter
from aiogram.types import Message, ContentType


class SupportedMediaFilter(BaseFilter):
    """
    This class is a custom filter for aiogram that checks if a message contains supported media types.

    It inherits from the BaseFilter class provided by aiogram.

    The __call__ method is overridden to provide the custom filtering logic.
    """

    async def __call__(self, message: Message) -> bool:
        """
        This method is an asynchronous method that checks if the content type of a message is among the supported media types.

        It is called when the filter is applied to a message.

        Args:
            message (Message): The message object that is being filtered.

        Returns:
            bool: True if the content type of the message is among the supported media types, False otherwise.
        """
        return message.content_type in (
            ContentType.ANIMATION, ContentType.AUDIO, ContentType.DOCUMENT,
            ContentType.PHOTO, ContentType.VIDEO, ContentType.VOICE
        )
