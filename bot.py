import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot import setup_routers
from bot.config import TOKEN_TELEGRAM
from bot.middlewares.I10n import L10nMiddleware
from bot.utils.fluent_helper import FluentDispenser


async def main():
    bot = Bot(
        token=TOKEN_TELEGRAM,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=MemoryStorage())

    router = setup_routers()
    dp.include_routers(router)

    from db.base import db
    await db.create_indexes()

    dispenser = FluentDispenser(
        locales_dir=Path(__file__).parent.joinpath("bot/locales"),
        default_language="en"
    )
    dp.update.middleware(L10nMiddleware(dispenser))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass