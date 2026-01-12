import os
import json
import base64
import gspread


def get_gspread_client():
    b64 = os.getenv("GOOGLE_CREDENTIALS_B64")

    if not b64:
        raise RuntimeError("GOOGLE_CREDENTIALS_B64 is not set")

    creds_json = base64.b64decode(b64).decode("utf-8")
    creds_dict = json.loads(creds_json)

    return gspread.service_account_from_dict(creds_dict)