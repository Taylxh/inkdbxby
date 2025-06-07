import gspread
from oauth2client.service_account import ServiceAccountCredentials
from constants import TRACKER_SHEET_NAME
import os
from datetime import datetime

# Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_path = "august-strata-461702g8-0315be2e0965.json"
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(os.getenv("INKDBXBY_CONTENT_VAULT")).worksheet(TRACKER_SHEET_NAME)

# Lookup user row
def get_user_row(user_id):
    records = sheet.get_all_records()
    for idx, row in enumerate(records, start=2):  # start=2 skips headers
        if str(row.get("user_id")) == str(user_id):
            return idx, row
    return None, None

# Public: Get user data by ID
def get_user_data(user_id):
    _, row = get_user_row(user_id)
    return row

# Public: Update or create fan memory
def update_user_data(user_id, username=None, kink=None, amount=None):
    idx, row = get_user_row(user_id)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if row:  # Update existing row
        if username:
            sheet.update_cell(idx, 2, username)

        if kink:
            existing = row.get("kinks", "")
            kink_list = [k.strip() for k in existing.split(",") if k.strip()]
            if kink not in kink_list:
                kink_list.append(kink)
                updated_kinks = ", ".join(kink_list)
                sheet.update_cell(idx, 3, updated_kinks)

        if amount:
            try:
                current_spend = float(row.get("total_spent", 0)) or 0
            except:
                current_spend = 0
            updated_spend = current_spend + amount
            sheet.update_cell(idx, 4, updated_spend)

        sheet.update_cell(idx, 5, now)  # last interaction
    else:  # Add new fan
        sheet.append_row([
            str(user_id),
            username or "",
            kink or "",
            amount or 0,
            now
        ])

# Public: Check if user spent over X
def has_spent_over(user_id, threshold):
    row = get_user_data(user_id)
    if not row:
        return False
    try:
        return float(row.get("total_spent", 0)) >= threshold
    except:
        return False
