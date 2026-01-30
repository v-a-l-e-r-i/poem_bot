from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import os

from keyboards.admin import admin_panel_keyboard

ADMIN_IDS = {int(x) for x in os.getenv("ADMIN_IDS").split(",")}

router_admin = Router()

@router_admin.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    await message.answer(
        "🔐 Адмін-панель",
        reply_markup=admin_panel_keyboard()
    )

