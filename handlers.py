from telegram.ext import MessageHandler, filters, CallbackQueryHandler
from logic import handle_message, handle_callback

def register_handlers(app):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))
