import os
from datetime import time

# Telegram bot token (set this in Render as an environment variable)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Google Sheet tab names
VAULT_SHEET_NAME = "Vault"
PROOF_SHEET_NAME = "Proof"
TRACKER_SHEET_NAME = "Tracker"

# Silent hours (AEST timezone)
SILENT_HOURS = {
    "Monday": (time(1, 30), time(6, 0)),
    "Tuesday": (time(1, 30), time(6, 0)),
    "Wednesday": (time(1, 30), time(6, 0)),
    "Thursday": (time(1, 30), time(6, 0)),
    "Friday": (time(3, 30), time(8, 0)),     # Friday night / Saturday morning
    "Saturday": (time(3, 30), time(7, 30)),  # Saturday night / Sunday morning
    "Sunday": (time(1, 30), time(6, 0))
}

# Blocked/taboo kink keywords
BLOCKED_KINKS = [
    "raceplay", "blood", "knife", "scat", "piss", "vomit", "noncon", "pedo", "underage",
    "beast", "animal", "incest", "daddy play", "hypno", "chloroform", "forced"
]

# Trigger phrases that activate menu responses
MENU_TRIGGERS = [
    "menu", "price list", "send me your menu", "content menu", "prices", "taster menu", 
    "vault menu", "custom menu", "what can I buy", "show me your menu", "send menu"
]
