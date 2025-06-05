import gspread
from oauth2client.service_account import ServiceAccountCredentials
from constants import VAULT_SHEET_NAME, PROOF_SHEET_NAME, TRACKER_SHEET_NAME
import os
from datetime import datetime

# Google Sheets auth setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_path = os.getenv("GOOGLE_SHEETS_KEY")
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(os.getenv("INKDBXBY_CONTENT_VAULT"))

vault_sheet = sheet.worksheet(VAULT_SHEET_NAME)
proof_sheet = sheet.worksheet(PROOF_SHEET_NAME)
tracker_sheet = sheet.worksheet(TRACKER_SHEET_NAME)

# Get all content items from the Vault
def get_vault_items():
    return vault_sheet.get_all_records()

# Log a proof of payment screenshot
def save_proof(user_id, username, filename):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    proof_sheet.append_row([str(user_id), username, filename, timestamp])

# Update or log spend in Tracker
def update_spend(user_id, username, amount):
    records = tracker_sheet.get_all_records()
    found = False
    for idx, row in enumerate(records, start=2):
        if str(row.get("user_id")) == str(user_id):
            current_spend = float(row.get("total_spent", 0)) or 0
            updated_spend = current_spend + amount
            tracker_sheet.update_cell(idx, 4, updated_spend)
            found = True
            break

    if not found:
        tracker_sheet.append_row([
            str(user_id),
            username or "",
            "",
            amount
        ])
