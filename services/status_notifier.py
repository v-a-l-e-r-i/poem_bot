import asyncio
import os
import random
import time
from datetime import datetime

from gspread.exceptions import APIError

from keyboards.submission import send_work_keyboard
from services.google_auth import get_gspread_client
from services.status_checker import check_statuses_and_update
from gspread.utils import ValueInputOption
from utils.logger import setup_logger

logger = setup_logger()

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
            logger.warning(
                "Google Sheets API error on attempt %s/%s: %s",
                attempt, retries, e
            )

            if attempt == retries:
                raise

            sleep_time = 2 ** attempt + random.uniform(0, 1)
            time.sleep(sleep_time)

async def process_status_updates(bot):
    logger.info("Processing status updates started")

    updates = await asyncio.to_thread(lambda: list(check_statuses_and_update()))
    logger.info("Found %d updates to process", len(updates))

    for item in updates:
        user_id = item["user_id"]
        status = item["status"]
        row_index = item["row_index"]

        logger.info(
            "Sending status notification to user_id=%s (status=%s)",
            user_id,
            status
        )

        try:
            if status == "accepted":
                text = (
                    "Вітаємо тебе, авторе! 🫶🏻\n"
                    "Твоя творчість буде у каналі Провулку!\n"
                    "Дякуємо!"
                )
            else:
                text = (
                    "На жаль, твій твір не було прийнято.\n"
                    "Проте не журися — наступного разу все вийде!"
                )

            await bot.send_message(user_id, text)

            logger.info(
                "Message successfully sent to user_id=%s",
                user_id
            )

        except Exception as e:
            logger.error(
                "Failed to send message to user_id=%s",
                user_id,
                exc_info=e
            )
            continue

        try:
            await asyncio.to_thread(update_decision_date, row_index)
            logger.info(
                "decision_date updated for row %d",
                row_index
            )
        except Exception as e:
            logger.error(
                "Failed to update decision_date for row %d",
                row_index,
                exc_info=e
            )

        # оновлюємо decision_date
        await asyncio.to_thread(update_decision_date, row_index)

    logger.info("Processing status updates finished")





def update_decision_date(row_index: int):
    from datetime import datetime

    ws = get_worksheet()

    ws.update_cell(
        row_index,
        8,  # decision date column (H)
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
