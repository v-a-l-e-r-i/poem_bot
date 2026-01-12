import os

import gspread

from services.google_auth import get_gspread_client
from utils.logger import setup_logger
from dotenv import load_dotenv

load_dotenv()
logger = setup_logger()

def get_worksheet():
    """
    Повертає worksheet Google Sheets
    """
    gc = get_gspread_client()
    sh = gc.open_by_key(os.getenv("SPREADSHEET_ID"))
    ws = sh.sheet1
    return ws

def check_statuses_and_update():
    logger.info("Status check started")

    ws = get_worksheet()

    rows = ws.get_all_records()
    logger.info("Fetched %d rows from Google Sheets", len(rows))

    for index, row in enumerate(rows, start=2):
        user_id = row.get("user_id")
        status = row.get("status")
        decision_date = row.get("decision_date")

        if not user_id:
            logger.warning("Row %d skipped: missing user_id", index)
            continue

        if decision_date:
            logger.debug(
                "Row %d skipped: already processed (decision_date=%s)",
                index,
                decision_date
            )
            continue

        if status not in ("accepted", "rejected"):
            logger.debug(
                "Row %d skipped: status=%s",
                index,
                status
            )
            continue

        logger.info(
            "Row %d ready for notification (user_id=%s, status=%s)",
            index,
            user_id,
            status
        )

        yield {
            "row_index": index,
            "user_id": user_id,
            "status": status
        }

    logger.info("Status check finished")
