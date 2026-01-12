import asyncio
from datetime import datetime

from keyboards.submission import send_work_keyboard
from services.google_auth import get_gspread_client
from services.status_checker import check_statuses_and_update
from gspread.utils import ValueInputOption
from utils.logger import setup_logger

logger = setup_logger()


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
    import gspread
    from datetime import datetime

    gc = get_gspread_client()
    sh = gc.open_by_key("1cEwVqRIuimqNKGlnZut-X07DeLSYffLRPNDf0EAjDtc")
    ws = sh.sheet1

    ws.update_cell(
        row_index,
        8,  # decision_date column (H)
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
