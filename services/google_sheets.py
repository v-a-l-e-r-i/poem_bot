import gspread
from gspread.utils import ValueInputOption

def append_submission(submission_data: dict):
    gc = gspread.service_account("service_account.json")
    sh = gc.open_by_key("1cEwVqRIuimqNKGlnZut-X07DeLSYffLRPNDf0EAjDtc")
    ws = sh.sheet1

    row = [
        submission_data["user_id"],
        submission_data["username"],
        submission_data["work_content"],
        submission_data["author_name"],
        submission_data["social_links"],
        submission_data["submit_date"],
        submission_data["status"],
        submission_data["decision_date"],
    ]

    ws.append_row(row)


