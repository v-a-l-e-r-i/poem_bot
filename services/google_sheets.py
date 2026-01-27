import random
import time
from datetime import datetime

import gspread
from gspread.exceptions import APIError
from gspread.utils import ValueInputOption
from services.content_hash import make_content_hash
from dotenv import load_dotenv
import os

from services.google_auth import get_gspread_client
from utils.logger import setup_logger

logger = setup_logger()


load_dotenv()

def get_worksheet(retries: int = 3):
    spreadsheet_id = os.getenv("SPREADSHEET_ID")
    if not spreadsheet_id:
        raise RuntimeError("SPREADSHEET_ID is not set")

    gc = get_gspread_client()

    for attempt in range(1, retries + 1):
        try:
            sh = gc.open_by_key(spreadsheet_id)
            ws = sh.sheet1
            return ws

        except APIError as e:
            if attempt == retries:
                logger.error("Google Sheets unavailable after retries")
                return []

            wait = 5 * (attempt + 1) + random.uniform(0, 3)
            logger.warning(f"Retry {attempt + 1}/3, waiting {wait:.1f}s")
            time.sleep(wait)


# ─────────────────────────────────────────────
# 🔁 ПЕРЕВІРКА НА ДУБЛІКАТ КОНТЕНТУ
# ─────────────────────────────────────────────

def content_exists(content_hash: str) -> bool:
    """
    Перевіряє, чи вже існує такий content_hash у таблиці
    Колонка I (9) — content_hash
    """
    ws = get_worksheet()

    try:
        hashes = ws.col_values(9)[1:]  # без заголовка
        return content_hash in hashes
    except Exception as e:
        logger.error("Error checking duplicates", exc_info=e)
        return False


# ─────────────────────────────────────────────
# 📝 ЗАПИС НОВОЇ РОБОТИ
# ─────────────────────────────────────────────

def append_submission(submission_data: dict):
    """
    Додає новий рядок у таблицю
    Очікує submission_data з ключами за ТЗ
    """
    ws = get_worksheet()

    content_hash = make_content_hash(submission_data["work_content"])

    # 🔒 Захист від дублікатів
    if content_exists(content_hash):
        logger.warning("Duplicate content detected, skipping insert")
        return False

    row = [
        submission_data["user_id"],
        submission_data["username"],
        submission_data["work_content"],
        submission_data["author_name"],
        submission_data["social_links"],
        submission_data["submit_date"],
        submission_data["status"],
        submission_data["decision_date"],
        content_hash,
    ]

    try:
        ws.append_row(
            row,
            value_input_option=ValueInputOption.user_entered
        )
        logger.info("Submission appended to Google Sheets")
        return True

    except Exception as e:
        logger.error("Error appending submission", exc_info=e)
        return False


# ─────────────────────────────────────────────
# ✏️ ОНОВЛЕННЯ decision_date
# ─────────────────────────────────────────────

def update_decision_date(row_index: int):
    """
    Записує decision_date після відправки повідомлення користувачу
    Колонка H (8)
    """
    ws = get_worksheet()

    try:
        ws.update_cell(
            row_index,
            8,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        print(f"🕒 decision_date updated for row {row_index}")

    except Exception as e:
        logger.error("Error updating decision_date:", exc_info=e)


def append_submission_safe(submission_data: dict) -> bool:
    try:
        return append_submission(submission_data)
    except APIError as e:
        logger.exception("Google Sheets API error while appending submission")
        return False
    except Exception:
        logger.exception("Unexpected error while appending submission")
        return False
