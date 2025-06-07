from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from logic import TRIGGERS, TABOO_WORDS, PRICES
from memory import update_user_data, get_user_data
from sheets import save_proof, update_spend
from utils import get_user_identity
import os

# Main fallback message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id, username = get_user_identity(update)
    message_text = update.message.text.lower()

    # Taboo filter
    if any(word in message_text for word in TABOO_WORDS):
        await update.message.reply_text("That kind of request is strictly off limits. Don't ask again.")
        return

    # Track kinks
    for trigger in TRIGGERS["kink"]:
        if trigger in message_text:
            kink = message_text.replace(trigger, "").strip()
            update_user_data(user_id, username=username, kink=kink)
            await update.message.reply_text(f"Mmm, noted. I’ll keep that in mind for next time.")
            return

    # Proof handling
    for trigger in TRIGGERS["proof"]:
        if trigger in message_text and update.message.photo:
            photo_file = await update.message.photo[-1].get_file()
            file_path = f"proof_{user_id}.jpg"
            await photo_file.download_to_drive(file_path)
            save_proof(user_id, username, file_path)
            await update.message.reply_text("Proof received. Let’s get filthy.")
            return

    # Praise kink recall
    for trigger in TRIGGERS["memory"]:
        data = get_user_data(user_id)
        if data and data.get("kinks"):
            await update.message.reply_text(f"You like {data['kinks'].strip()}... naughty. I didn’t forget.")
        else:
            await update.message.reply_text("Tell me what turns you on. I like remembering dirty things.")
        return

    # Vault upsell suggestion (based on spend)
    if "vault" in message_text or any(w in message_text for w in TRIGGERS["vault"]):
        data = get_user_data(user_id)
        total_spent = float(data.get("total_spent", 0)) if data else 0

        if total_spent >= 100:
            await update.message.reply_text("You’ve unlocked Full Fantasy Vault access. Ask and it’s yours.")
        elif total_spent >= 40:
            await update.message.reply_text("You’ve got access to the Quickie & Wet Vaults. Want a peek?")
        else:
            await update.message.reply_text(
                "Vault bundles are waiting... tease tiers start at $40. Ask me about the Mystery Menu."
            )
        return

    # Tip triggers
    for trigger in TRIGGERS["tip"]:
        await update.message.reply_text("Tips don’t go unnoticed. You know how to get my attention.")
        return

    # Catch-all flirt reply
    await update.message.reply_text("Keep talking, babe. I’m listening... and I remember everything.")
    

# Export the handler
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
