from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_panel_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🖼 Переглянути зображення",
                    callback_data="admin_view_images"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎵 Переглянути музику",
                    callback_data="admin_view_music"
                )
            ]
        ]
    )
