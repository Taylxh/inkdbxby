import os
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Set up Google Sheets auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
key_path = "service_account/august-strata-461702-g8-2f6c2eddf4de.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
client = gspread.authorize(credentials)

# Your Google Sheet ID is loaded from Render's environment variable
VAULT_SHEET_ID = os.getenv("INKDBXBY_CONTENT_VAULT")

def get_vault_preview(tier):
    try:
        sheet = client.open_by_key(VAULT_SHEET_ID).worksheet(tier)
        previews = sheet.col_values(2)[1:]  # assumes previews are in column B
        return "\n".join(previews) if previews else None
    except:
        return None

def check_payment_proof(user_id):
    try:
        sheet = client.open_by_key(VAULT_SHEET_ID).worksheet("Proof Sheet")
        data = sheet.get_all_records()
        for row in data:
            if str(user_id) in str(row.get("TelegramID", "")):
                return True
        return False
    except:
        return False

def get_fan_rank(user_id):
    try:
        sheet = client.open_by_key(VAULT_SHEET_ID).worksheet("Fan Memory")
        data = sheet.get_all_records()
        for row in data:
            if str(user_id) in str(row.get("TelegramID", "")):
                return row.get("Rank", "Unknown")
        return "Unknown"
    except:
        return "Unknown"
