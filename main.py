from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.menu import menu_handler
from handlers.custom import custom_handler
from logic import handle_message
from constants import BOT_TOKEN

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Menu & custom routes
    app.add_handler(menu_handler)
    app.add_handler(custom_handler)

    # General fallback handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Nova is now running as the Inkdbxby bot...")
    app.run_polling()

if __name__ == "__main__":
    main()
