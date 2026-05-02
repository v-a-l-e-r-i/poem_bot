import asyncio

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from keyboards.submission import submission_type_keyboard, send_work_keyboard, permission_keyboard
from states.submission import SubmissionStates

from services.google_sheets import append_submission, append_submission_safe
import gspread

from utils.logger import setup_logger

logger = setup_logger()

router = Router()

CONTENT_TYPES = {
    "send_poetry": {
        "label": "поезію ✍️",
        "type": "poetry"
    },
    "send_prose": {
        "label": "прозу 📖",
        "type": "prose"
    },
    "send_visual": {
        "label": "візуальне мистецтво 🎨",
        "type": "visual"
    },
    "send_music": {
        "label": "музику 🎵",
        "type": "audio"
    },
    "send_other": {
        "label": "інше ✨",
        "type": "other"
    }
}


@router.callback_query(lambda c: c.data == "start_submission")
async def restart_submission(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.answer(
        "Обери, що саме ти хочеш нам надіслати ✨",
        reply_markup=submission_type_keyboard()
    )

    await callback.answer()


# Натискання кнопки "Надіслати поезію"
@router.callback_query(lambda c: c.data in CONTENT_TYPES)
async def start_submission(callback: CallbackQuery, state: FSMContext):
    content = CONTENT_TYPES[callback.data]

    await state.update_data(
        content_type=content["type"]
    )

    msg_text = f"Надішли свою {content['label']}"
    # Додаємо підказку для візуального мистецтва
    if content["type"] == "visual":
        msg_text += "\n(Рекомендуємо надсилати ілюстрацію у HD якості файлом png/jpg 🖼️)"

    await callback.message.answer(msg_text)
    await state.set_state(SubmissionStates.waiting_for_poem)
    await callback.answer()

# Отримання вірша
@router.message(SubmissionStates.waiting_for_poem)
async def receive_content(message: Message, state: FSMContext):
    content_value = None

    if message.text:
        content_value = f"text:{message.text}"
    elif message.photo:
        file_id = message.photo[-1].file_id
        content_value = f"photo:{file_id}"
    elif message.audio:
        content_value = f"audio:{message.audio.file_id}"
    elif message.voice:
        content_value = f"voice:{message.voice.file_id}"
    elif message.document:
        content_value = f"document:{message.document.file_id}"
    else:
        await message.answer("Будь ласка, надішли текст, фото, аудіо або файл 🙏")
        return

    await state.update_data(work_content=content_value)

    await message.answer(
        "Ми отримали твою творчість!\n"
        "Тепер напиши назву свого твору 📝\n"
        "(Якщо назви немає, напиши \"-\")"
    )
    await state.set_state(SubmissionStates.waiting_for_title)

@router.message(SubmissionStates.waiting_for_title)
async def receive_title(message: Message, state: FSMContext):
    await state.update_data(work_title=message.text)

    await message.answer(
        "Супер!\n"
        "Тепер напиши, як тебе підписати 🥰"
    )
    await state.set_state(SubmissionStates.waiting_for_name)

# Отримання імені
@router.message(SubmissionStates.waiting_for_name)
async def receive_name(message: Message, state: FSMContext):
    await state.update_data(author_name=message.text)

    await message.answer(
        "Гарне ім'я!\n"
        "Якщо бажаєш залишити свої соціальні мережі з творчістю – зроби це!\n"
        "(Якщо не маєш – напиши \"-\")"
    )

    await state.set_state(SubmissionStates.waiting_for_socials)


# Отримання соцмереж
# Змінюємо запит соцмереж, щоб з'явилися кнопки
@router.message(SubmissionStates.waiting_for_socials)
async def receive_socials(message: Message, state: FSMContext):
    await state.update_data(social_links=message.text)

    await message.answer(
        "Чи дозволяєте Ви опублікувати свою роботу в наших соціальних мережах, окрім Telegram-каналу?",
        reply_markup=permission_keyboard()
    )
    await state.set_state(SubmissionStates.waiting_for_permission)

@router.callback_query(SubmissionStates.waiting_for_permission)
async def receive_permission(callback: CallbackQuery, state: FSMContext):
    # Відсіюємо будь-які інші кнопки, крім Так і Ні
    if callback.data not in ["perm_yes", "perm_no"]:
        return

    # Визначаємо символ
    permission_symbol = "✅" if callback.data == "perm_yes" else "❌"

    # Зберігаємо символ в стан
    await state.update_data(publish_permission=permission_symbol)
    data = await state.get_data()

    submission_data = {
        "user_id": callback.from_user.id,
        "username": callback.from_user.username or "",
        "work_content": data.get("work_content"),
        "work_title": data.get("work_title"),
        "author_name": data.get("author_name"),
        "social_links": data.get("social_links"),
        "publish_permission": data.get("publish_permission"),
        "submit_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "pending",
        "decision_date": ""
    }

    try:
        success = await asyncio.to_thread(
            append_submission_safe,
            submission_data
        )
    except Exception as e:
        logger.exception("Failed to save submission to Google Sheets")
        success = False

    if not success:
        await callback.message.answer(
            "Схоже, цю роботу вже надсилали раніше 🤍\n"
            "Ми не можемо прийняти один і той самий твір двічі.\n\n"
            "Якщо хочеш — надішли іншу роботу,\n"
            "або трохи відредагуй цю й спробуй ще раз ✨",
            reply_markup=send_work_keyboard()
        )
        await state.clear()
        await callback.answer()
        return

    await callback.message.answer(
        "Дякую!\n"
        "В найближчому часі ми повідомимо тобі!\n"
        "До нових зустрічей, друже 🫶🏻",
        reply_markup=send_work_keyboard()
    )

    await state.clear()
    await callback.answer() # Прибирає годинник завантаження на кнопці