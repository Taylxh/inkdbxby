# handlers.py
from telegram.ext import MessageHandler, CallbackQueryHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from logic import handle_triggered_response
from handlers.menu import handle_menu_selection
from memory import update_fan_memory

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.effective_user.id
    text = update.message.text.strip().lower()

    # Update memory with latest message
    await update_fan_memory(user_id, text)

    # Pass message to logic.py trigger handler
    response = await handle_triggered_response(update, context, text)

    if response:
        await update.message.reply_text(response)

def register_handlers(application):
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_handler(CallbackQueryHandler(handle_menu_selection))
