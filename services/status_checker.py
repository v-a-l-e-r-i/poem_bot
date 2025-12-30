import gspread
from datetime import datetime
from gspread.utils import ValueInputOption


def check_statuses_and_update():
    gc = gspread.service_account("service_account.json")
    sh = gc.open_by_key("1cEwVqRIuimqNKGlnZut-X07DeLSYffLRPNDf0EAjDtc")
    ws = sh.sheet1

    rows = ws.get_all_records()

    for index, row in enumerate(rows, start=2):
        user_id = row.get("user_id")
        status = row.get("status")
        decision_date = row.get("decision_date")

        # ❗ якщо вже є decision_date — НЕ ЧІПАЄМО
        if decision_date:
            continue

        # ❗ якщо ще не прийнято/відхилено — теж пропускаємо
        if status not in ("accepted", "rejected"):
            continue

        yield {
            "row_index": index,
            "user_id": user_id,
            "status": status
        }
