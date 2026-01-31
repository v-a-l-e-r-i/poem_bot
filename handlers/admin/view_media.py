import asyncio

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram import F
from services.google_sheets import get_worksheet
from utils.logger import setup_logger

logger = setup_logger()
router_admin = Router()

@router_admin.callback_query(F.data == "admin_view_images")
async def view_images(callback: CallbackQuery):
    logger.info("Admin clicked view images")

    try:
        ws = get_worksheet()
        rows = ws.get_all_records()
    except Exception:
        logger.exception("Failed to load images")
        await callback.message.answer("Помилка при завантаженні 😔")
        await callback.answer()
        return


    images = [
        r for r in rows
        if r.get("work_content").split(":")[0] == "photo" and r.get("work_content")
    ]

    if not images:
        await callback.message.answer("Немає зображень 😔")
        await callback.answer()
        return

    try:
        for row in images:
            # Отримуємо "сирий" контент
            content = row.get("work_content", "")

            # Розділяємо безпечно (максимум 1 раз)
            parts = content.split(":", 1)

            if len(parts) < 2:
                logger.warning(f"Incorrect data format: {content}")
                continue

            # .strip() - це головне виправлення. Воно прибирає пробіли з країв
            file_id = parts[1].strip()

            # Логуємо, щоб бачити, що відправляємо (для відладки)
            logger.info(f"Attempt to send photo with ID: '{file_id}'")

            try:
                await callback.bot.send_photo(
                    chat_id=callback.from_user.id,
                    photo=file_id,
                    caption=f"Author: {row.get('author_name', '-')}"
                )
                # Робимо маленьку паузу, щоб не отримати FloodWait, якщо фото багато
                await asyncio.sleep(0.3)

            except Exception as e:
                logger.warning(f"Failed to send photo {file_id}: {e}")
                await callback.message.answer(f"Помилка з фото автора {row.get('author_name')}")

    except Exception as e:
        logger.exception("Critical error in the sending cycle")


    await callback.answer()


@router_admin.callback_query(F.data == "admin_view_music")
async def view_music(callback: CallbackQuery):
    logger.info("Admin clicked view music")

    try:
        ws = get_worksheet()
        rows = ws.get_all_records()
    except Exception:
        logger.exception("Failed to load music")
        await callback.message.answer("Помилка при завантаженні 😔")
        await callback.answer()
        return

    # Фільтруємо записи, шукаємо і audio, і voise (та voice про всяк випадок)
    # Використовуємо startswith для надійності
    music = [
        r for r in rows
        if r.get("work_content") and (
                str(r.get("work_content")).startswith("audio:") or
                str(r.get("work_content")).startswith("voice:")
        )
    ]

    if not music:
        await callback.message.answer("Немає музики/декламацій 😔")
        await callback.answer()
        return

    try:
        for row in music:
            content = row.get("work_content", "")
            parts = content.split(":", 1)

            if len(parts) < 2:
                continue

            content_type = parts[0]  # "audio", "voise" або "voice"
            file_id = parts[1].strip()  # Прибираємо пробіли

            logger.info(f"Attempt to send {content_type} with ID: '{file_id}'")

            try:
                author_caption = f"Автор: {row.get('author_name', '-')}"

                # РОЗГАЛУЖЕННЯ: Відправляємо правильний тип медіа
                if content_type == "audio":
                    await callback.bot.send_audio(
                        chat_id=callback.from_user.id,
                        audio=file_id,
                        caption=author_caption
                    )
                elif content_type == "voice":
                    await callback.bot.send_voice(
                        chat_id=callback.from_user.id,
                        voice=file_id,
                        caption=author_caption
                    )
                else:
                    logger.warning(f"Невідомий тип контенту: {content_type}")

                # Пауза, щоб уникнути FloodWait
                await asyncio.sleep(0.3)

            except Exception as e:
                logger.warning(f"Failed to send {content_type} {file_id}: {e}")
                # Можна не спамити повідомленнями про помилку користувачу,
                # але якщо хочете бачити, де помилка - розкоментуйте рядок нижче:
                # await callback.message.answer(f"Помилка з файлом автора {row.get('author_name')}")

    except Exception as e:
        logger.exception("Critical error in the music sending cycle")

    await callback.answer()
