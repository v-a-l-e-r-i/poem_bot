import gspread
from utils.logger import setup_logger

logger = setup_logger()


def check_statuses_and_update():
    logger.info("Status check started")

    gc = gspread.service_account("service_account.json")
    sh = gc.open("Провулок")
    ws = sh.sheet1

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
