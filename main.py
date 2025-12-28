import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from handlers.submission import router as submission_router

from keyboards.submission import submission_type_keyboard

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start_handler(message: Message):
    await message.answer(
        "Вітаю у Провулку! 🌙\n\n"
        "Надішли нам свою творчість ✨\n"
        "(вірш, верлібр, проза, візуальне мистецтво)"
        "Оберіть, що саме ви хочете нам надіслати:",
        reply_markup=submission_type_keyboard()
    )


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, CommandStart())
    dp.include_router(submission_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
