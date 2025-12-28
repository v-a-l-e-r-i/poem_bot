from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def submission_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✍️ Надіслати поезію", callback_data="send_poetry")],
            [InlineKeyboardButton(text="📖 Надіслати прозу", callback_data="send_prose")],
            [InlineKeyboardButton(text="🎨 Надіслати візуальне мистецтво", callback_data="send_visual")],
            [InlineKeyboardButton(text="🎵 Надіслати музику", callback_data="send_music")],
            [InlineKeyboardButton(text="✨ Надіслати інше", callback_data="send_other")],
            [InlineKeyboardButton(text="❓ Поставити питання", callback_data="ask_question")],
        ]
    )
