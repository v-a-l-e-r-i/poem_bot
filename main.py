import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from handlers.router import root_router

from keyboards.submission import send_work_keyboard
from services.status_notifier import process_status_updates

from utils.logger import setup_logger

logger = setup_logger()


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start_handler(message: Message):
    await message.answer(
        "Вітаю у Провулку! 🌙\n\n"
        "Надішли нам свою творчість ✨\n"
        "(вірш, верлібр, проза, візуальне мистецтво)"
        "Оберіть, що саме ви хочете нам надіслати:",
        reply_markup=send_work_keyboard()
    )
    logger.info("Bot started 🚀")



async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, CommandStart())
    dp.include_router(root_router)


    async def scheduler():
        while True:
            try:
                await process_status_updates(bot)
            except Exception as e:
                logger.exception("Scheduler error (Google Sheets may be unavailable)")
            finally:
                await asyncio.sleep(3600)

    asyncio.create_task(scheduler())


    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
