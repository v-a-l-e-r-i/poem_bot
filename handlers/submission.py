from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from states.submission import SubmissionStates

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
        "type": "music"
    },
    "send_other": {
        "label": "інше ✨",
        "type": "other"
    }
}

# Натискання кнопки "Надіслати поезію"
@router.callback_query(lambda c: c.data in CONTENT_TYPES)
async def start_submission(callback: CallbackQuery, state: FSMContext):
    content = CONTENT_TYPES[callback.data]

    await state.update_data(
        content_type=content["type"]
    )

    await callback.message.answer(
        f"Надішли свою {content['label']}"
    )

    await state.set_state(SubmissionStates.waiting_for_poem)
    await callback.answer()

# Отримання вірша
@router.message(SubmissionStates.waiting_for_poem)
async def receive_poem(message: Message, state: FSMContext):
    await state.update_data(
        work_content=message.text
    )

    await message.answer(
        "Ми отримали твою творчість!\n"
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
@router.message(SubmissionStates.waiting_for_socials)
async def receive_socials(message: Message, state: FSMContext):
    await state.update_data(social_links=message.text)

    data = await state.get_data()

    submission_data = {
        "user_id": message.from_user.id,
        "username": message.from_user.username or "",
        "work_content": data.get("work_content"),
        "author_name": data.get("author_name"),
        "social_links": data.get("social_links"),
        "submit_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "pending",
        "decision_date": ""
    }

    # 🔹 ПОКИ ЩО — просто дивимось, що зберігається
    print("DATA FOR TABLE:")
    for k, v in submission_data.items():
        print(f"{k}: {v}")

    await message.answer(
        "Дякую!\n"
        "В найближчому часі ми повідомимо тебе!\n"
        "До нових зустрічей, друже 🫶🏻"
    )

    await state.clear()
