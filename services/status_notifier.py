import asyncio
from datetime import datetime
from services.status_checker import check_statuses_and_update
from gspread.utils import ValueInputOption


async def process_status_updates(bot):
    updates = await asyncio.to_thread(lambda: list(check_statuses_and_update()))

    for item in updates:
        user_id = item.get("user_id")
        if not user_id:
            continue

        status = item["status"]
        row_index = item["row_index"]

        if status == "accepted":
            text = (
                "Вітаємо тебе, авторе! 🫶🏻\n"
                "Твоя творчість буде у каналі Провулку!\n"
                "Публікація може зайняти від однієї до трьох діб.\n"
                "Дякуємо!"
            )
        else:
            text = (
                "На жаль, твій твір не було прийнято.\n"
                "Проте не журися — наступного разу все вийде!"
            )

        try:
            await bot.send_message(user_id, text)
        except Exception as e:
            print("Telegram send error:", e)

        # оновлюємо decision_date
        await asyncio.to_thread(update_decision_date, row_index)


def update_decision_date(row_index: int):
    import gspread
    from datetime import datetime

    gc = gspread.service_account("service_account.json")
    sh = gc.open_by_key("1cEwVqRIuimqNKGlnZut-X07DeLSYffLRPNDf0EAjDtc")
    ws = sh.sheet1

    ws.update_cell(
        row_index,
        8,  # decision_date column (H)
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
