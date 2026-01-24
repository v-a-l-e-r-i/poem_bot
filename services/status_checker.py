import os
import random
import time

import gspread

from services.google_auth import get_gspread_client
from utils.logger import setup_logger
from dotenv import load_dotenv
from gspread.exceptions import APIError

load_dotenv()
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


def check_statuses_and_update():
    logger.info("Status check started")

    ws = get_worksheet()

    rows = ws.get_all_records()
    logger.info("Fetched %d rows from Google Sheets", len(rows))
    VALID_STATUSES = {"pending", "accepted", "rejected"}

    for index, row in enumerate(rows, start=2):
        user_id = row.get("user_id")
        status = str(row.get("status", "")).strip().lower()
        decision_date = str(row.get("decision_date", "")).strip()

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

        if status not in VALID_STATUSES:
            logger.warning(
                "Invalid status value: %r at row %s",
                row.get("status"),
                index
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
