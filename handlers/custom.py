from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from logic import TRIGGERS, PRICES

# Respond to fans asking for a custom
async def handle_custom_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.lower()
    for trigger in TRIGGERS["custom"]:
        if trigger in message_text:
            await update.message.reply_photo(
                photo=open("media/custom_menu.jpg", "rb"),
                caption=(
                    "Custom content is available if you're serious.\n\n"
                    f"Basic custom pic or voice note: ${PRICES['custom_pic_voice']}\n"
                    f"Custom video scene: starts at ${PRICES['custom_scene']}\n"
                    f"Rush fee for same-day delivery: ${PRICES['rush_fee']}\n\n"
                    "All customs must be paid upfront with screenshot proof.\n"
                    "Send your request in detail along with payment proof to proceed."
                ),
                parse_mode="Markdown"
            )
            return

# Register the custom request handler
custom_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_request)
